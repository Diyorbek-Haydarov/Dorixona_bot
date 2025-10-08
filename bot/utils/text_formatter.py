"""
Text formatting utilities
"""

from ..config import LANG_LATIN, LANG_CYRILLIC, Texts

def format_medicine_info(medicine: dict, user_language: str) -> str:
    """Format medicine information for display"""
    if user_language == LANG_CYRILLIC:
        name = medicine.get('name_cyrillic', medicine.get('name_latin', 'N/A'))
        description = medicine.get('description_cyrillic', medicine.get('description_latin', 'Ma\'lumot yo\'q'))
        composition = medicine.get('composition_cyrillic', medicine.get('composition_latin', 'Ma\'lumot yo\'q'))
        usage = medicine.get('usage_cyrillic', medicine.get('usage_latin', 'Ma\'lumot yo\'q'))
        side_effects = medicine.get('side_effects_cyrillic', medicine.get('side_effects_latin', 'Ma\'lumot yo\'q'))
        
        template = Texts.MEDICINE_INFO_CYRILLIC
    else:
        name = medicine.get('name_latin', medicine.get('name_cyrillic', 'N/A'))
        description = medicine.get('description_latin', medicine.get('description_cyrillic', 'Ma\'lumot yo\'q'))
        composition = medicine.get('composition_latin', medicine.get('composition_cyrillic', 'Ma\'lumot yo\'q'))
        usage = medicine.get('usage_latin', medicine.get('usage_cyrillic', 'Ma\'lumot yo\'q'))
        side_effects = medicine.get('side_effects_latin', medicine.get('side_effects_cyrillic', 'Ma\'lumot yo\'q'))
        
        template = Texts.MEDICINE_INFO_LATIN
    
    return template.format(
        name=name,
        description=description,
        composition=composition,
        usage=usage,
        side_effects=side_effects
    )

def format_first_aid_article(article: dict, user_language: str) -> str:
    """Format first aid article for display"""
    if user_language == LANG_CYRILLIC:
        title = article.get('title_cyrillic', article.get('title_latin', 'N/A'))
        content = article.get('content_cyrillic', article.get('content_latin', 'Ma\'lumot yo\'q'))
    else:
        title = article.get('title_latin', article.get('title_cyrillic', 'N/A'))
        content = article.get('content_latin', article.get('content_cyrillic', 'Ma\'lumot yo\'q'))
    
    return f"🚑 **{title}**\n\n{content}"

def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to specified length"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."

def escape_markdown(text: str) -> str:
    """Escape special characters for Markdown"""
    special_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for char in special_chars:
        text = text.replace(char, f'\\{char}')
    return text

def format_contact_info(user_language: str) -> str:
    """Format contact information"""
    if user_language == LANG_CYRILLIC:
        return Texts.CONTACT_INFO_CYRILLIC
    else:
        return Texts.CONTACT_INFO_LATIN

def format_error_message(user_language: str) -> str:
    """Format error message"""
    if user_language == LANG_CYRILLIC:
        return Texts.ERROR_CYRILLIC
    else:
        return Texts.ERROR_LATIN
