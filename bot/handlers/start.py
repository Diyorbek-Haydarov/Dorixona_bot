"""
Start command handler
"""

import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from ..database import db
from ..config import LANG_LATIN, LANG_CYRILLIC, Texts, Buttons
from ..keyboards.main_menu import get_language_keyboard, get_main_menu_keyboard

logger = logging.getLogger(__name__)
router = Router()

@router.message(CommandStart())
async def start_command(message: Message, state: FSMContext):
    """Handle /start command"""
    try:
        user_id = message.from_user.id
        username = message.from_user.username
        first_name = message.from_user.first_name
        
        # Add user to database
        await db.add_user(user_id, username, first_name)
        
        # Get user's current language
        user_language = await db.get_user_language(user_id)
        
        if user_language:
            # User already has language preference, show main menu
            await show_main_menu(message, user_language)
        else:
            # New user, show language selection
            await show_language_selection(message)
            
    except Exception as e:
        logger.error(f"Error in start command: {e}")
        await message.answer(Texts.ERROR_LATIN)

@router.message(Command("help"))
async def help_command(message: Message):
    """Handle /help command"""
    try:
        user_id = message.from_user.id
        user_language = await db.get_user_language(user_id)
        
        if user_language == LANG_CYRILLIC:
            help_text = Texts.WELCOME_CYRILLIC
        else:
            help_text = Texts.WELCOME_LATIN
            
        await message.answer(help_text, reply_markup=get_main_menu_keyboard(user_language))
        
    except Exception as e:
        logger.error(f"Error in help command: {e}")
        await message.answer(Texts.ERROR_LATIN)

@router.callback_query(F.data == "select_language_latin")
async def select_language_latin(callback: CallbackQuery, state: FSMContext):
    """Handle Latin language selection"""
    try:
        user_id = callback.from_user.id
        
        # Set user language
        await db.set_user_language(user_id, LANG_LATIN)
        
        # Show confirmation and main menu
        await callback.message.edit_text(
            Texts.LANGUAGE_SELECTED_LATIN,
            reply_markup=get_main_menu_keyboard(LANG_LATIN)
        )
        
        await callback.answer()
        
    except Exception as e:
        logger.error(f"Error selecting Latin language: {e}")
        await callback.answer(Texts.ERROR_LATIN, show_alert=True)

@router.callback_query(F.data == "select_language_cyrillic")
async def select_language_cyrillic(callback: CallbackQuery, state: FSMContext):
    """Handle Cyrillic language selection"""
    try:
        user_id = callback.from_user.id
        
        # Set user language
        await db.set_user_language(user_id, LANG_CYRILLIC)
        
        # Show confirmation and main menu
        await callback.message.edit_text(
            Texts.LANGUAGE_SELECTED_CYRILLIC,
            reply_markup=get_main_menu_keyboard(LANG_CYRILLIC)
        )
        
        await callback.answer()
        
    except Exception as e:
        logger.error(f"Error selecting Cyrillic language: {e}")
        await callback.answer(Texts.ERROR_CYRILLIC, show_alert=True)

@router.callback_query(F.data == "main_menu")
async def back_to_main_menu(callback: CallbackQuery):
    """Handle back to main menu"""
    try:
        user_id = callback.from_user.id
        user_language = await db.get_user_language(user_id)
        
        if user_language == LANG_CYRILLIC:
            welcome_text = Texts.WELCOME_CYRILLIC
        else:
            welcome_text = Texts.WELCOME_LATIN
            
        await callback.message.edit_text(
            welcome_text,
            reply_markup=get_main_menu_keyboard(user_language)
        )
        
        await callback.answer()
        
    except Exception as e:
        logger.error(f"Error returning to main menu: {e}")
        await callback.answer(Texts.ERROR_LATIN, show_alert=True)

async def show_language_selection(message: Message):
    """Show language selection keyboard"""
    try:
        await message.answer(
            "Tilni tanlang / Выберите язык:",
            reply_markup=get_language_keyboard()
        )
    except Exception as e:
        logger.error(f"Error showing language selection: {e}")

async def show_main_menu(message: Message, user_language: str):
    """Show main menu with user's language"""
    try:
        if user_language == LANG_CYRILLIC:
            welcome_text = Texts.WELCOME_CYRILLIC
        else:
            welcome_text = Texts.WELCOME_LATIN
            
        await message.answer(
            welcome_text,
            reply_markup=get_main_menu_keyboard(user_language)
        )
    except Exception as e:
        logger.error(f"Error showing main menu: {e}")
