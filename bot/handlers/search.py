"""
Medicine search handler
"""

import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from ..database import db
from ..config import LANG_LATIN, LANG_CYRILLIC, Texts, Buttons
from ..keyboards.main_menu import get_main_menu_keyboard
from ..utils.text_formatter import format_medicine_info

logger = logging.getLogger(__name__)
router = Router()

@router.callback_query(F.data == "search_medicine")
async def search_medicine_callback(callback: CallbackQuery, state: FSMContext):
    """Handle search medicine button click"""
    try:
        user_id = callback.from_user.id
        user_language = await db.get_user_language(user_id)
        
        if user_language == LANG_CYRILLIC:
            prompt_text = Texts.SEARCH_PROMPT_CYRILLIC
        else:
            prompt_text = Texts.SEARCH_PROMPT_LATIN
            
        await callback.message.edit_text(
            prompt_text,
            reply_markup=get_back_keyboard(user_language)
        )
        
        # Set state to waiting for search query
        await state.set_state("waiting_for_search")
        await callback.answer()
        
    except Exception as e:
        logger.error(f"Error in search medicine callback: {e}")
        await callback.answer(Texts.ERROR_LATIN, show_alert=True)

@router.message(F.text, lambda message, state: state.get_state() == "waiting_for_search")
async def handle_search_query(message: Message, state: FSMContext):
    """Handle medicine search query"""
    try:
        user_id = message.from_user.id
        user_language = await db.get_user_language(user_id)
        query = message.text.strip()
        
        logger.info(f"Search query from user {user_id}: '{query}', language: {user_language}")
        
        if not query:
            if user_language == LANG_CYRILLIC:
                error_text = Texts.SEARCH_PROMPT_CYRILLIC
            else:
                error_text = Texts.SEARCH_PROMPT_LATIN
            await message.answer(error_text)
            return
        
        # Search for medicine
        medicine = await db.search_medicine(query, user_language)
        logger.info(f"Search result: {medicine is not None}")
        
        if medicine:
            # Increment search count
            await db.increment_search_count()
            
            # Format and send medicine information
            medicine_text = format_medicine_info(medicine, user_language)
            
            # Create keyboard with voice button if available
            keyboard = create_medicine_keyboard(medicine, user_language)
            
            await message.answer(
                medicine_text,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
        else:
            # No results found
            if user_language == LANG_CYRILLIC:
                no_results_text = Texts.NO_RESULTS_CYRILLIC
            else:
                no_results_text = Texts.NO_RESULTS_LATIN
                
            await message.answer(
                no_results_text,
                reply_markup=get_back_keyboard(user_language)
            )
        
        # Clear state
        await state.clear()
        
    except Exception as e:
        logger.error(f"Error handling search query: {e}")
        await message.answer(Texts.ERROR_LATIN)
        await state.clear()

@router.message(F.text)
async def handle_direct_search(message: Message):
    """Handle direct medicine search without using search button"""
    try:
        # Skip if this is a command or if user is in a different state
        if message.text.startswith('/'):
            return
            
        user_id = message.from_user.id
        user_language = await db.get_user_language(user_id)
        query = message.text.strip()
        
        # Only search if the query looks like a medicine name (not too long, not too short)
        if len(query) < 2 or len(query) > 50:
            return
            
        logger.info(f"Direct search query from user {user_id}: '{query}', language: {user_language}")
        
        # Search for medicine
        medicine = await db.search_medicine(query, user_language)
        
        if medicine:
            # Increment search count
            await db.increment_search_count()
            
            # Format and send medicine information
            medicine_text = format_medicine_info(medicine, user_language)
            
            # Create keyboard with voice button if available
            keyboard = create_medicine_keyboard(medicine, user_language)
            
            await message.answer(
                medicine_text,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
        
    except Exception as e:
        logger.error(f"Error handling direct search: {e}")

@router.callback_query(F.data.startswith("voice_"))
async def send_voice_message(callback: CallbackQuery):
    """Handle voice message request"""
    try:
        user_id = callback.from_user.id
        user_language = await db.get_user_language(user_id)
        
        # Extract medicine_id from callback data
        medicine_id = int(callback.data.replace("voice_", ""))
        
        # Get medicine details to get voice_file_id
        medicine = await db.get_medicine_by_id(medicine_id)
        
        if medicine and medicine.get('voice_file_id'):
            # Send voice message
            await callback.bot.send_voice(
                chat_id=callback.message.chat.id,
                voice=medicine['voice_file_id']
            )
            
            if user_language == LANG_CYRILLIC:
                await callback.answer("Овозли тавсиф юборилди")
            else:
                await callback.answer("Ovozli tavsif yuborildi")
        else:
            if user_language == LANG_CYRILLIC:
                await callback.answer("Овозли тавсиф мавжуд эмас", show_alert=True)
            else:
                await callback.answer("Ovozli tavsif mavjud emas", show_alert=True)
        
    except Exception as e:
        logger.error(f"Error sending voice message: {e}")
        await callback.answer(Texts.ERROR_LATIN, show_alert=True)

def get_back_keyboard(user_language: str) -> InlineKeyboardMarkup:
    """Create back to main menu keyboard"""
    if user_language == LANG_CYRILLIC:
        back_text = Buttons.BACK_CYRILLIC
    else:
        back_text = Buttons.BACK_LATIN
        
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=back_text, callback_data="main_menu")]
    ])
    return keyboard

def create_medicine_keyboard(medicine: dict, user_language: str) -> InlineKeyboardMarkup:
    """Create keyboard for medicine information"""
    buttons = []
    
    # Add voice button if available
    if medicine.get('voice_file_id'):
        if user_language == LANG_CYRILLIC:
            voice_text = "🎵 Овозли тавсиф"
        else:
            voice_text = "🎵 Ovozli tavsif"
        buttons.append([InlineKeyboardButton(
            text=voice_text,
            callback_data=f"voice_{medicine['id']}"
        )])
    
    # Add back button
    if user_language == LANG_CYRILLIC:
        back_text = Buttons.BACK_CYRILLIC
    else:
        back_text = Buttons.BACK_LATIN
    buttons.append([InlineKeyboardButton(text=back_text, callback_data="main_menu")])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)
