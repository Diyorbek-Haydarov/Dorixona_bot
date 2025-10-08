"""
Configuration settings for PharmaGuide Bot
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot Configuration
BOT_TOKEN = os.getenv('BOT_TOKEN')
PRIVATE_CHANNEL_ID = os.getenv('PRIVATE_CHANNEL_ID')

# Database Configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///pharma_bot.db')

# Admin Configuration
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin123')

# Flask Configuration
FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'your-secret-key-here')
FLASK_ENV = os.getenv('FLASK_ENV', 'development')

# Logging Configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = os.getenv('LOG_FILE', 'pharma_bot.log')

# Bot Settings
ITEMS_PER_PAGE = 10
MAX_SEARCH_RESULTS = 5

# Language Codes
LANG_LATIN = 'uz_latin'
LANG_CYRILLIC = 'uz_cyrillic'

# Button Texts
class Buttons:
    # Latin Script
    SEARCH_MEDICINE_LATIN = "💊 Dori qidirish"
    MEDICINES_LIST_LATIN = "📖 Dorilar ro'yxati"
    FIRST_AID_LATIN = "🚑 Birinchi yordam"
    CONTACT_LATIN = "📞 Aloqa"
    SETTINGS_LATIN = "⚙️ Sozlamalar"
    BACK_LATIN = "⬅️ Orqaga"
    NEXT_LATIN = "➡️ Keyingi"
    PREVIOUS_LATIN = "⬅️ Oldingi"
    CHANGE_LANGUAGE_LATIN = "🌐 Tilni o'zgartirish"
    
    # Cyrillic Script
    SEARCH_MEDICINE_CYRILLIC = "💊 Дори қидириш"
    MEDICINES_LIST_CYRILLIC = "📖 Дорилар рўйхати"
    FIRST_AID_CYRILLIC = "🚑 Биринчи ёрдам"
    CONTACT_CYRILLIC = "📞 Алоқа"
    SETTINGS_CYRILLIC = "⚙️ Созламалар"
    BACK_CYRILLIC = "⬅️ Орқага"
    NEXT_CYRILLIC = "➡️ Кейинги"
    PREVIOUS_CYRILLIC = "⬅️ Олдинги"
    CHANGE_LANGUAGE_CYRILLIC = "🌐 Тилни ўзгартириш"

# User Messages
class Texts:
    # Welcome Messages
    WELCOME_LATIN = """Assalomu alaykum! 👋

Men PharmaGuide bot - sizning tibbiy ma'lumotlar yordamchingiz.

Men sizga quyidagi xizmatlarni taklif qilaman:
• 💊 Dori qidirish
• 📖 Dorilar ro'yxati
• 🚑 Birinchi yordam
• 📞 Shifokorlar bilan aloqa

Tilni tanlang:"""
    
    WELCOME_CYRILLIC = """Ассалому алайкум! 👋

Мен PharmaGuide бот - сизнинг тиббий маълумотлар ёрдамчингиз.

Мен сизга қуйидаги хизматларни таклиф қиламан:
• 💊 Дори қидириш
• 📖 Дорилар рўйхати
• 🚑 Биринчи ёрдам
• 📞 Шифокорлар билан алоқа

Тилни танланг:"""
    
    # Language Selection
    LANGUAGE_SELECTED_LATIN = "✅ Til tanlandi: O'zbek (Lotin)"
    LANGUAGE_SELECTED_CYRILLIC = "✅ Тил танланди: Ўзбек (Кирилл)"
    
    # Search Messages
    SEARCH_PROMPT_LATIN = "🔍 Qidirish uchun dori nomini yuboring:"
    SEARCH_PROMPT_CYRILLIC = "🔍 Қидириш учун дори номини юборинг:"
    
    NO_RESULTS_LATIN = "❌ Hech qanday natija topilmadi. Boshqa nom bilan urinib ko'ring."
    NO_RESULTS_CYRILLIC = "❌ Ҳеч қандай натижа топилмади. Бошқа ном билан уриниб кўринг."
    
    # Medicine Information
    MEDICINE_INFO_LATIN = """💊 **{name}**

📝 **Tavsif:**
{description}

🧪 **Tarkibi:**
{composition}

💡 **Qo'llash:**
{usage}

⚠️ **Yon ta'sirlar:**
{side_effects}"""
    
    MEDICINE_INFO_CYRILLIC = """💊 **{name}**

📝 **Тавсиф:**
{description}

🧪 **Таркиби:**
{composition}

💡 **Қўллаш:**
{usage}

⚠️ **Ён таъсирлар:**
{side_effects}"""
    
    # First Aid
    FIRST_AID_TITLE_LATIN = "🚑 Birinchi yordam"
    FIRST_AID_TITLE_CYRILLIC = "🚑 Биринчи ёрдам"
    
    # Contact
    CONTACT_INFO_LATIN = """📞 **Shifokorlar bilan aloqa**

🏥 **Tez yordam:** 103
🏥 **Poliklinika:** +998 71 123-45-67
🏥 **Shifokor maslahati:** +998 90 123-45-67

⚠️ **Muhim:** Favqulodda holatda darhol tez yordamga murojaat qiling!"""
    
    CONTACT_INFO_CYRILLIC = """📞 **Шифокорлар билан алоқа**

🏥 **Тез ёрдам:** 103
🏥 **Поликлиника:** +998 71 123-45-67
🏥 **Шифокор маслахати:** +998 90 123-45-67

⚠️ **Муҳим:** Фавқулодда ҳолатда дарҳол тез ёрдамга мурожаат қилинг!"""
    
    # Settings
    SETTINGS_LATIN = "⚙️ **Sozlamalar**\n\nTilni o'zgartirish uchun tugmani bosing:"
    SETTINGS_CYRILLIC = "⚙️ **Созламалар**\n\nТилни ўзгартириш учун тугмани босинг:"
    
    # Error Messages
    ERROR_LATIN = "❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring."
    ERROR_CYRILLIC = "❌ Хатолик юз берди. Илтимос, қайтадан уриниб кўринг."
    
    # Voice Messages
    VOICE_AVAILABLE_LATIN = "🎵 Ovozli tavsif mavjud"
    VOICE_AVAILABLE_CYRILLIC = "🎵 Овозли тавсиф мавжуд"
    
    VOICE_NOT_AVAILABLE_LATIN = "🎵 Ovozli tavsif mavjud emas"
    VOICE_NOT_AVAILABLE_CYRILLIC = "🎵 Овозли тавсиф мавжуд эмас"

# Admin Messages
class AdminTexts:
    LOGIN_REQUIRED = "Please log in to access this page."
    INVALID_CREDENTIALS = "Invalid username or password."
    LOGIN_SUCCESS = "Successfully logged in."
    LOGOUT_SUCCESS = "Successfully logged out."
    
    # Medicine Management
    MEDICINE_ADDED = "Medicine added successfully."
    MEDICINE_UPDATED = "Medicine updated successfully."
    MEDICINE_DELETED = "Medicine deleted successfully."
    
    # First Aid Management
    FIRST_AID_ADDED = "First aid article added successfully."
    FIRST_AID_UPDATED = "First aid article updated successfully."
    FIRST_AID_DELETED = "First aid article deleted successfully."
    
    # Validation Messages
    REQUIRED_FIELD = "This field is required."
    INVALID_FORMAT = "Invalid format."
