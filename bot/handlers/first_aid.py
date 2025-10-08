"""
First aid handler
"""

import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from ..database import db
from ..config import LANG_LATIN, LANG_CYRILLIC, Buttons
from ..keyboards.main_menu import get_main_menu_keyboard

logger = logging.getLogger(__name__)
router = Router()

@router.callback_query(F.data == "first_aid")
async def show_first_aid_menu(callback: CallbackQuery):
    """Show first aid menu"""
    try:
        user_id = callback.from_user.id
        user_language = await db.get_user_language(user_id)
        
        # Get first aid articles
        articles = await db.get_first_aid_articles()
        
        if not articles:
            if user_language == LANG_CYRILLIC:
                message_text = "Биринчи ёрдам мақолалари мавжуд эмас"
            else:
                message_text = "Birinchi yordam maqolalari mavjud emas"
        else:
            # Format first aid articles
            message_text = format_first_aid_list(articles, user_language)
        
        # Create keyboard with articles
        keyboard = create_first_aid_keyboard(articles, user_language)
        
        await callback.message.edit_text(
            message_text,
            reply_markup=keyboard,
            parse_mode="Markdown"
        )
        
        await callback.answer()
        
    except Exception as e:
        logger.error(f"Error showing first aid menu: {e}")
        await callback.answer("Xatolik yuz berdi", show_alert=True)

@router.callback_query(F.data.startswith("first_aid_"))
async def show_first_aid_article(callback: CallbackQuery):
    """Show specific first aid article"""
    try:
        user_id = callback.from_user.id
        user_language = await db.get_user_language(user_id)
        
        # Extract article ID from callback data
        article_id = int(callback.data.replace("first_aid_", ""))
        
        # Get first aid articles
        articles = await db.get_first_aid_articles()
        
        # Find the specific article
        article = None
        for art in articles:
            if art['id'] == article_id:
                article = art
                break
        
        if article:
            # Format article content
            article_text = format_first_aid_article(article, user_language)
            
            # Create back keyboard
            keyboard = create_first_aid_back_keyboard(user_language)
            
            await callback.message.edit_text(
                article_text,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
        else:
            if user_language == LANG_CYRILLIC:
                await callback.answer("Мақола топилмади", show_alert=True)
            else:
                await callback.answer("Maqola topilmadi", show_alert=True)
        
        await callback.answer()
        
    except Exception as e:
        logger.error(f"Error showing first aid article: {e}")
        await callback.answer("Xatolik yuz berdi", show_alert=True)

def format_first_aid_list(articles: list, user_language: str) -> str:
    """Format first aid articles list"""
    if user_language == LANG_CYRILLIC:
        header = "🚑 **Биринчи ёрдам**\n\n"
    else:
        header = "🚑 **Birinchi yordam**\n\n"
    
    article_list = []
    for i, article in enumerate(articles, 1):
        if user_language == LANG_CYRILLIC:
            title = article.get('title_cyrillic', article.get('title_latin', 'N/A'))
        else:
            title = article.get('title_latin', article.get('title_cyrillic', 'N/A'))
        
        article_list.append(f"{i}. {title}")
    
    return header + "\n".join(article_list)

def format_first_aid_article(article: dict, user_language: str) -> str:
    """Format individual first aid article"""
    if user_language == LANG_CYRILLIC:
        title = article.get('title_cyrillic', article.get('title_latin', 'N/A'))
        content = article.get('content_cyrillic', article.get('content_latin', 'N/A'))
    else:
        title = article.get('title_latin', article.get('title_cyrillic', 'N/A'))
        content = article.get('content_latin', article.get('content_cyrillic', 'N/A'))
    
    return f"🚑 **{title}**\n\n{content}"

def create_first_aid_keyboard(articles: list, user_language: str) -> InlineKeyboardMarkup:
    """Create keyboard for first aid articles"""
    buttons = []
    
    # Add article buttons
    for article in articles:
        if user_language == LANG_CYRILLIC:
            title = article.get('title_cyrillic', article.get('title_latin', 'N/A'))
        else:
            title = article.get('title_latin', article.get('title_cyrillic', 'N/A'))
        
        # Truncate long titles
        display_title = title[:40] + "..." if len(title) > 40 else title
        buttons.append([InlineKeyboardButton(
            text=display_title,
            callback_data=f"first_aid_{article['id']}"
        )])
    
    # Add back button
    if user_language == LANG_CYRILLIC:
        back_text = Buttons.BACK_CYRILLIC
    else:
        back_text = Buttons.BACK_LATIN
    buttons.append([InlineKeyboardButton(text=back_text, callback_data="main_menu")])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def create_first_aid_back_keyboard(user_language: str) -> InlineKeyboardMarkup:
    """Create back keyboard for first aid articles"""
    if user_language == LANG_CYRILLIC:
        back_text = "⬅️ Рўйхатга қайтиш"
    else:
        back_text = "⬅️ Ro'yxatga qaytish"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=back_text, callback_data="first_aid")],
        [InlineKeyboardButton(text=Buttons.BACK_CYRILLIC if user_language == LANG_CYRILLIC else Buttons.BACK_LATIN, callback_data="main_menu")]
    ])
    return keyboard
