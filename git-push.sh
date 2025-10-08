#!/usr/bin/env bash
set -e

# ==== GITHUB PUSH AUTOMATION SCRIPT ====
# Author: Diyorbek versiyasi
# Bu skript loyiha papkasidan GitHub'ga kodlarni avtomatik yuklaydi.

# Rangli chiqishlar
GREEN="\033[0;32m"
RED="\033[0;31m"
YELLOW="\033[1;33m"
RESET="\033[0m"

echo -e "${GREEN}🚀 GitHub push avtomatlashtirish skripti ishga tushdi${RESET}"

# 1. Foydalanuvchidan repo URL va commit so‘rash
read -p "🔗 GitHub SSH URL kiriting (masalan: git@github.com:Diyorbek-Haydarov/Dorixona_bot.git): " REMOTE
read -p "💬 Commit xabari (default: 'Auto commit'): " MESSAGE
MESSAGE=${MESSAGE:-"Auto commit"}

# 2. Tekshirish: .git mavjudmi?
if [ -d .git ]; then
    echo -e "${YELLOW}⚠️  Eski Git repozitoriya topildi, davom etamiz...${RESET}"
else
    echo -e "${GREEN}🆕 Yangi Git repozitoriya yaratilmoqda...${RESET}"
    git init
fi

# 3. Fayllarni qo‘shish va commit qilish
git add .
git commit -m "$MESSAGE" || echo -e "${YELLOW}⚠️  O‘zgarish yo‘q, commit o'tkazib yuborildi${RESET}"

# 4. Remote sozlash
if git remote get-url origin >/dev/null 2>&1; then
    echo -e "${YELLOW}🔄 Remote yangilanmoqda...${RESET}"
    git remote set-url origin "$REMOTE"
else
    echo -e "${GREEN}🔗 Remote qo‘shilmoqda...${RESET}"
    git remote add origin "$REMOTE"
fi

# 5. Branch nomini main deb o‘rnatish
git branch -M main

# 6. Push qilish
echo -e "${GREEN}☁️  GitHub'ga push qilinmoqda...${RESET}"
git push -u origin main

echo -e "${GREEN}✅ Kodlar GitHub'ga muvaffaqiyatli yuklandi!${RESET}"
