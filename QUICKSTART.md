# 🚀 PharmaGuide Bot - Quick Start Guide

Get your PharmaGuide Bot up and running in 5 minutes!

## ⚡ Quick Setup

### 1. Prerequisites
- Python 3.8 or higher
- Git (optional, for cloning)

### 2. One-Command Setup

**Linux/Mac:**
```bash
./setup.sh
```

**Windows:**
```cmd
setup.bat
```

### 3. Configure Your Bot

1. Edit `.env` file:
```env
BOT_TOKEN=your_telegram_bot_token_here
PRIVATE_CHANNEL_ID=-1001234567890
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your_secure_password
```

2. Get your bot token from [@BotFather](https://t.me/botfather)

### 4. Start the Bot

**Linux/Mac:**
```bash
./run_bot.sh
```

**Windows:**
```cmd
run_bot.bat
```

### 5. Start Admin Panel

**Linux/Mac:**
```bash
./run_admin.sh
```

**Windows:**
```cmd
run_admin.bat
```

Open browser: http://localhost:5000

## 🎯 First Steps

### 1. Login to Admin Panel
- Username: `admin`
- Password: `admin123` (change this!)

### 2. Add Your First Medicine
1. Go to "Medicines" → "Add Medicine"
2. Fill in both Latin and Cyrillic fields
3. Click "Add Medicine"

### 3. Test the Bot
1. Find your bot on Telegram
2. Send `/start`
3. Select language
4. Try searching for your medicine

## 🔧 Configuration

### Bot Settings
Edit `bot/config.py`:
```python
ITEMS_PER_PAGE = 10  # Medicines per page
MAX_SEARCH_RESULTS = 5  # Max search results
```

### Language Support
The bot supports:
- Uzbek Latin (O'zbek)
- Uzbek Cyrillic (Ўзбек)

## 📱 Bot Commands

- `/start` - Start the bot and select language
- `/help` - Show help information

## 🎵 Voice Messages

To add voice descriptions:

1. Record audio description
2. Send to your private Telegram channel
3. Forward to [@userinfobot](https://t.me/userinfobot)
4. Copy the file_id
5. Paste in admin panel medicine form

## 🚑 First Aid Articles

Add emergency instructions:

1. Go to "First Aid" → "Add Article"
2. Fill in both languages
3. Select category
4. Save

## 📊 Admin Features

- **Dashboard** - Statistics and recent users
- **Medicines** - Full CRUD operations
- **First Aid** - Emergency articles management
- **Bilingual** - All content in both scripts

## 🔒 Security

### Change Default Password
```bash
python init_admin.py
```

### Environment Variables
Never commit `.env` file to version control!

## 🐛 Troubleshooting

### Bot Won't Start
1. Check bot token in `.env`
2. Verify Python version (3.8+)
3. Check logs: `pharma_bot.log`

### Admin Login Fails
1. Reset password: `python init_admin.py`
2. Check database: `pharma_bot.db`

### Voice Messages Don't Work
1. Verify bot is admin in private channel
2. Check `PRIVATE_CHANNEL_ID` format (include minus sign)
3. Test with simple message first

## 📈 Next Steps

1. **Add More Medicines** - Use admin panel
2. **Customize Messages** - Edit `bot/config.py`
3. **Add Voice Descriptions** - Follow voice setup guide
4. **Deploy to Production** - See deployment guide

## 🆘 Need Help?

1. Check `README.md` for detailed documentation
2. Review `FILE_CHECKLIST.md` for complete file list
3. Check logs for error messages
4. Verify all requirements are installed

## 🎉 You're Ready!

Your PharmaGuide Bot is now running with:
- ✅ Bilingual interface
- ✅ Medicine search
- ✅ Voice messages
- ✅ First aid articles
- ✅ Admin panel
- ✅ User statistics

**Happy coding! 🚀**
