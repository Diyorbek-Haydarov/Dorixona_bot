"""
Main menu keyboards
"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from ..config import LANG_LATIN, LANG_CYRILLIC, Buttons

def get_language_keyboard() -> InlineKeyboardMarkup:
    """Create language selection keyboard"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🇺🇿 O'zbek (Lotin)",
                callback_data="select_language_latin"
            )
        ],
        [
            InlineKeyboardButton(
                text="🇺🇿 Ўзбек (Кирилл)",
                callback_data="select_language_cyrillic"
            )
        ]
    ])
    return keyboard

def get_main_menu_keyboard(user_language: str) -> InlineKeyboardMarkup:
    """Create main menu keyboard based on user language"""
    if user_language == LANG_CYRILLIC:
        buttons = [
            [
                InlineKeyboardButton(
                    text=Buttons.SEARCH_MEDICINE_CYRILLIC,
                    callback_data="search_medicine"
                )
            ],
            [
                InlineKeyboardButton(
                    text=Buttons.MEDICINES_LIST_CYRILLIC,
                    callback_data="medicines_list"
                )
            ],
            [
                InlineKeyboardButton(
                    text=Buttons.FIRST_AID_CYRILLIC,
                    callback_data="first_aid"
                )
            ],
            [
                InlineKeyboardButton(
                    text=Buttons.CONTACT_CYRILLIC,
                    callback_data="contact"
                )
            ],
            [
                InlineKeyboardButton(
                    text=Buttons.SETTINGS_CYRILLIC,
                    callback_data="settings"
                )
            ]
        ]
    else:
        buttons = [
            [
                InlineKeyboardButton(
                    text=Buttons.SEARCH_MEDICINE_LATIN,
                    callback_data="search_medicine"
                )
            ],
            [
                InlineKeyboardButton(
                    text=Buttons.MEDICINES_LIST_LATIN,
                    callback_data="medicines_list"
                )
            ],
            [
                InlineKeyboardButton(
                    text=Buttons.FIRST_AID_LATIN,
                    callback_data="first_aid"
                )
            ],
            [
                InlineKeyboardButton(
                    text=Buttons.CONTACT_LATIN,
                    callback_data="contact"
                )
            ],
            [
                InlineKeyboardButton(
                    text=Buttons.SETTINGS_LATIN,
                    callback_data="settings"
                )
            ]
        ]
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)
