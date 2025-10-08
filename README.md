# 💊 PharmaGuide Bot - Uzbek Medical Information Bot

A comprehensive Telegram bot providing medical information in both Uzbek Latin and Cyrillic scripts.

## ✨ Features

### User Features
- 🔍 **Medicine Search** - Search medicines by name
- 📖 **Browse Medicines** - Paginated list of all medicines
- 🎵 **Voice Descriptions** - Audio descriptions via private channel
- 🚑 **First Aid** - Emergency medical instructions
- 📞 **Contact Info** - Specialist contact details
- ⚙️ **Settings** - Language switching (Latin/Cyrillic)
- 👤 **User Tracking** - Automatic user registration

### Admin Features
- 🔐 **Secure Login** - Password-protected admin panel
- 📊 **Dashboard** - Statistics and user analytics
- 💊 **Medicine Management** - Full CRUD operations
- 🚑 **First Aid Management** - Add/edit emergency articles
- 🌐 **Bilingual Support** - Manage content in both scripts
- 🎵 **Voice Integration** - Easy voice message management

## 🚀 Quick Start

### 1. Setup (One Time)
```bash
# Linux/Mac
./setup.sh

# Windows
setup.bat
```

### 2. Run the Bot
```bash
# Activate virtual environment
source venv/bin/activate  # Windows: venv\Scripts\activate

# Start bot
python run_bot.py
```

### 3. Run Admin Panel
```bash
# In new terminal
source venv/bin/activate  # Windows: venv\Scripts\activate

# Start admin panel
python run_admin.py

# Open browser: http://localhost:5000
```

## 📁 Project Structure

```
Apteka_bot/
├── .env.example              # Environment variables template
├── .gitignore               # Git ignore rules
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── QUICKSTART.md           # Quick setup guide
├── FILE_CHECKLIST.md       # Complete file list
├── PROJECT_COMPLETE.md     # Implementation summary
├── init_admin.py           # Admin user creation
├── sample_data.py          # Sample data population
├── run_bot.py              # Bot launcher
├── run_admin.py            # Admin panel launcher
├── setup.sh                # Linux/Mac setup script
├── setup.bat               # Windows setup script
├── bot/                    # Bot package
│   ├── __init__.py
│   ├── main.py             # Bot initialization
│   ├── config.py           # Configuration
│   ├── database.py         # Database operations
│   ├── handlers/           # Message handlers
│   │   ├── __init__.py
│   │   ├── start.py        # Start command
│   │   ├── search.py       # Search functionality
│   │   ├── medicines_list.py # Medicine browsing
│   │   ├── contact.py      # Contact info
│   │   ├── first_aid.py    # First aid
│   │   └── settings.py     # Settings
│   ├── keyboards/          # Button layouts
│   │   ├── __init__.py
│   │   └── main_menu.py    # Main menu buttons
│   └── utils/              # Utilities
│       ├── __init__.py
│       └── text_formatter.py # Text formatting
└── admin/                  # Admin panel
    ├── __init__.py
    ├── app.py              # Flask application
    └── templates/          # HTML templates
        ├── base.html       # Base template
        ├── login.html      # Login page
        ├── dashboard.html  # Dashboard
        ├── medicines_list.html # Medicine list
        ├── medicine_form.html  # Medicine form
        ├── first_aid_list.html # First aid list
        └── first_aid_form.html # First aid form
```

## 🔧 Configuration

### Environment Variables
Copy `.env.example` to `.env` and configure:

```env
BOT_TOKEN=your_telegram_bot_token
PRIVATE_CHANNEL_ID=-1001234567890
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your_secure_password
```

### Bot Settings
Edit `bot/config.py` to customize:
- Items per page
- Button texts
- User messages
- Language codes

## 📊 Database Schema

### Tables
1. **users** - User information and preferences
2. **medicines** - Medicine data (bilingual)
3. **first_aid** - Emergency instructions (bilingual)
4. **admin_users** - Admin authentication
5. **bot_stats** - Usage statistics

## 🌐 Languages Supported

- **Uzbek Latin** (uz_latin) - Default
- **Uzbek Cyrillic** (uz_cyrillic)

## 🔒 Security Features

- Password hashing with Werkzeug
- Environment variable protection
- SQL injection prevention
- Session management
- Input validation

## 📈 Scalability

- Async operations throughout
- Efficient database queries
- Pagination for large datasets
- Telegram file caching
- Comprehensive logging

## 🛠️ Development

### Adding New Features
1. Create handler in `bot/handlers/`
2. Add keyboard in `bot/keyboards/`
3. Update database schema if needed
4. Add admin panel support
5. Update documentation

### Code Quality
- Type hints throughout
- Comprehensive docstrings
- Error handling
- Logging system
- Clean architecture

## 📝 License

This project is open source. Please ensure medical information accuracy and include appropriate disclaimers.

## ⚠️ Medical Disclaimer

This bot provides general medical information only. Always consult healthcare professionals for medical advice, diagnosis, or treatment.

## 🤝 Support

For support and questions:
1. Check documentation files
2. Review code comments
3. Check logs: `pharma_bot.log`
4. Create an issue

---

**Made with ❤️ for the Uzbekistan developer community**
