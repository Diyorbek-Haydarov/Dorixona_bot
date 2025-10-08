"""
Contact information handler
"""

import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery

from ..database import db
from ..config import LANG_LATIN, LANG_CYRILLIC, Texts, Buttons
from ..keyboards.main_menu import get_main_menu_keyboard

logger = logging.getLogger(__name__)
router = Router()

@router.callback_query(F.data == "contact")
async def show_contact_info(callback: CallbackQuery):
    """Show contact information"""
    try:
        user_id = callback.from_user.id
        user_language = await db.get_user_language(user_id)
        
        if user_language == LANG_CYRILLIC:
            contact_text = Texts.CONTACT_INFO_CYRILLIC
        else:
            contact_text = Texts.CONTACT_INFO_LATIN
            
        await callback.message.edit_text(
            contact_text,
            reply_markup=get_main_menu_keyboard(user_language),
            parse_mode="Markdown"
        )
        
        await callback.answer()
        
    except Exception as e:
        logger.error(f"Error showing contact info: {e}")
        await callback.answer(Texts.ERROR_LATIN, show_alert=True)
