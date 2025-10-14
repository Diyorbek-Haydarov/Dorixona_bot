"""
Medicines list handler
"""

import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from ..database import db
from ..config import LANG_LATIN, LANG_CYRILLIC, Buttons, ITEMS_PER_PAGE
from ..keyboards.main_menu import get_main_menu_keyboard
from ..utils.text_formatter import format_medicine_info

logger = logging.getLogger(__name__)
router = Router()

@router.callback_query(F.data == "medicines_list")
async def show_medicines_list(callback: CallbackQuery):
    """Show paginated medicines list"""
    try:
        user_id = callback.from_user.id
        user_language = await db.get_user_language(user_id)
        
        # Get first page of medicines
        medicines = await db.get_medicines_paginated(page=1, per_page=ITEMS_PER_PAGE)
        total_medicines = await db.get_medicines_count()
        
        if not medicines:
            if user_language == LANG_CYRILLIC:
                message_text = "Дорилар рўйхати бўш"
            else:
                message_text = "Dorilar ro'yxati bo'sh"
        else:
            # Format medicines list
            message_text = format_medicines_list(medicines, user_language, 1, total_medicines)
        
        # Create pagination keyboard
        keyboard = create_pagination_keyboard(1, total_medicines, user_language, medicines)
        
        await callback.message.edit_text(
            message_text,
            reply_markup=keyboard,
            parse_mode="Markdown"
        )
        
        await callback.answer()
        
    except Exception as e:
        logger.error(f"Error showing medicines list: {e}")
        await callback.answer("Xatolik yuz berdi", show_alert=True)

@router.callback_query(F.data.startswith("page_"))
async def handle_page_navigation(callback: CallbackQuery):
    """Handle page navigation"""
    try:
        user_id = callback.from_user.id
        user_language = await db.get_user_language(user_id)
        
        # Extract page number from callback data
        page = int(callback.data.replace("page_", ""))
        
        # Get medicines for the requested page
        medicines = await db.get_medicines_paginated(page=page, per_page=ITEMS_PER_PAGE)
        total_medicines = await db.get_medicines_count()
        
        if medicines:
            # Format medicines list
            message_text = format_medicines_list(medicines, user_language, page, total_medicines)
            
            # Create pagination keyboard
            keyboard = create_pagination_keyboard(page, total_medicines, user_language, medicines)
            
            await callback.message.edit_text(
                message_text,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
        else:
            if user_language == LANG_CYRILLIC:
                await callback.answer("Бу саҳифада дорилар йўқ", show_alert=True)
            else:
                await callback.answer("Bu sahifada dorilar yo'q", show_alert=True)
        
        await callback.answer()
        
    except Exception as e:
        logger.error(f"Error handling page navigation: {e}")
        await callback.answer("Xatolik yuz berdi", show_alert=True)

@router.callback_query(F.data.startswith("medicine_"))
async def show_medicine_details(callback: CallbackQuery):
    """Show detailed medicine information"""
    try:
        user_id = callback.from_user.id
        user_language = await db.get_user_language(user_id)
        
        # Extract medicine ID from callback data
        medicine_id = int(callback.data.replace("medicine_", ""))
        
        # Get medicine details
        medicine = await db.get_medicine_by_id(medicine_id)
        
        if medicine:
            # Increment view count
            await db.increment_medicine_view_count()
            
            # Format medicine information
            medicine_text = format_medicine_info(medicine, user_language)
            
            # Create keyboard with voice button if available
            keyboard = create_medicine_detail_keyboard(medicine, user_language)
            
            await callback.message.edit_text(
                medicine_text,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
        else:
            if user_language == LANG_CYRILLIC:
                await callback.answer("Дори топилмади", show_alert=True)
            else:
                await callback.answer("Dori topilmadi", show_alert=True)
        
        await callback.answer()
        
    except Exception as e:
        logger.error(f"Error showing medicine details: {e}")
        await callback.answer("Xatolik yuz berdi", show_alert=True)

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
        
        await callback.answer()
        
    except Exception as e:
        logger.error(f"Error sending voice message: {e}")
        if user_language == LANG_CYRILLIC:
            await callback.answer("Овозли тавсиф юборишда хатолик", show_alert=True)
        else:
            await callback.answer("Ovozli tavsif yuborishda xatolik", show_alert=True)

def format_medicines_list(medicines: list, user_language: str, page: int, total: int) -> str:
    """Format medicines list for display"""
    if user_language == LANG_CYRILLIC:
        header = f"📖 **Дорилар рўйхати** (Саҳифа {page})\n\n"
    else:
        header = f"📖 **Dorilar ro'yxati** (Sahifa {page})\n\n"
    
    medicine_list = []
    for i, medicine in enumerate(medicines, 1):
        # Get medicine name in user's language
        if user_language == LANG_CYRILLIC:
            name = medicine.get('name_cyrillic', medicine.get('name_latin', 'N/A'))
        else:
            name = medicine.get('name_latin', medicine.get('name_cyrillic', 'N/A'))
        
        medicine_list.append(f"{i}. {name}")
    
    list_text = "\n".join(medicine_list)
    
    # Add pagination info
    start_item = (page - 1) * ITEMS_PER_PAGE + 1
    end_item = min(start_item + len(medicines) - 1, total)
    
    if user_language == LANG_CYRILLIC:
        footer = f"\n\n📊 {start_item}-{end_item} / {total} дори"
    else:
        footer = f"\n\n📊 {start_item}-{end_item} / {total} dori"
    
    return header + list_text + footer

def create_pagination_keyboard(page: int, total_medicines: int, user_language: str, medicines: list) -> InlineKeyboardMarkup:
    """Create pagination keyboard"""
    total_pages = (total_medicines + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE
    
    buttons = []
    
    # Add medicine buttons for current page
    for medicine in medicines:
        if user_language == LANG_CYRILLIC:
            name = medicine.get('name_cyrillic', medicine.get('name_latin', 'N/A'))
        else:
            name = medicine.get('name_latin', medicine.get('name_cyrillic', 'N/A'))
        
        # Truncate long names
        display_name = name[:30] + "..." if len(name) > 30 else name
        buttons.append([InlineKeyboardButton(
            text=display_name,
            callback_data=f"medicine_{medicine['id']}"
        )])
    
    # Add navigation buttons
    nav_buttons = []
    
    if page > 1:
        if user_language == LANG_CYRILLIC:
            prev_text = Buttons.PREVIOUS_CYRILLIC
        else:
            prev_text = Buttons.PREVIOUS_LATIN
        nav_buttons.append(InlineKeyboardButton(
            text=prev_text,
            callback_data=f"page_{page - 1}"
        ))
    
    if page < total_pages:
        if user_language == LANG_CYRILLIC:
            next_text = Buttons.NEXT_CYRILLIC
        else:
            next_text = Buttons.NEXT_LATIN
        nav_buttons.append(InlineKeyboardButton(
            text=next_text,
            callback_data=f"page_{page + 1}"
        ))
    
    if nav_buttons:
        buttons.append(nav_buttons)
    
    # Add back button
    if user_language == LANG_CYRILLIC:
        back_text = Buttons.BACK_CYRILLIC
    else:
        back_text = Buttons.BACK_LATIN
    buttons.append([InlineKeyboardButton(text=back_text, callback_data="main_menu")])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def create_medicine_detail_keyboard(medicine: dict, user_language: str) -> InlineKeyboardMarkup:
    """Create keyboard for medicine details"""
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
    
    # Add back to list button
    if user_language == LANG_CYRILLIC:
        back_text = "⬅️ Рўйхатга қайтиш"
    else:
        back_text = "⬅️ Ro'yxatga qaytish"
    buttons.append([InlineKeyboardButton(text=back_text, callback_data="medicines_list")])
    
    # Add main menu button
    if user_language == LANG_CYRILLIC:
        main_text = Buttons.BACK_CYRILLIC
    else:
        main_text = Buttons.BACK_LATIN
    buttons.append([InlineKeyboardButton(text=main_text, callback_data="main_menu")])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)
