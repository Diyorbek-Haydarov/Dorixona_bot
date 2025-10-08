"""
Settings handler
"""

import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery

from ..database import db
from ..config import LANG_LATIN, LANG_CYRILLIC, Texts, Buttons
from ..keyboards.main_menu import get_language_keyboard, get_main_menu_keyboard

logger = logging.getLogger(__name__)
router = Router()

@router.callback_query(F.data == "settings")
async def show_settings(callback: CallbackQuery):
    """Show settings menu"""
    try:
        user_id = callback.from_user.id
        user_language = await db.get_user_language(user_id)
        
        if user_language == LANG_CYRILLIC:
            settings_text = Texts.SETTINGS_CYRILLIC
        else:
            settings_text = Texts.SETTINGS_LATIN
            
        await callback.message.edit_text(
            settings_text,
            reply_markup=get_language_keyboard(),
            parse_mode="Markdown"
        )
        
        await callback.answer()
        
    except Exception as e:
        logger.error(f"Error showing settings: {e}")
        await callback.answer(Texts.ERROR_LATIN, show_alert=True)

@router.callback_query(F.data == "change_language")
async def change_language(callback: CallbackQuery):
    """Handle language change request"""
    try:
        user_id = callback.from_user.id
        user_language = await db.get_user_language(user_id)
        
        if user_language == LANG_CYRILLIC:
            settings_text = Texts.SETTINGS_CYRILLIC
        else:
            settings_text = Texts.SETTINGS_LATIN
            
        await callback.message.edit_text(
            settings_text,
            reply_markup=get_language_keyboard(),
            parse_mode="Markdown"
        )
        
        await callback.answer()
        
    except Exception as e:
        logger.error(f"Error changing language: {e}")
        await callback.answer(Texts.ERROR_LATIN, show_alert=True)
