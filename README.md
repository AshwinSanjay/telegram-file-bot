# 📁 Telegram File Bot

A Telegram bot built with Python using `pyTelegramBotAPI`.  
This bot allows the admin to upload any type of file, store it in a private server channel, and generate a public link. When users click the link, the bot checks if they are members of a required channel before sending the file.

---

## ✨ Features

- ✅ Admin-only file uploads
- 📤 Stores files in a private server channel
- 🔗 Auto-generates download links
- 👥 Requires users to join a specific channel before download
- 📎 Supports all file types (photos, videos, documents, audio)
- 🔒 Verifies channel membership using Telegram API
- 💾 Stores file references in JSON

---

## 🚀 Deploy to Render (Free Hosting)

### 1. Upload to GitHub

Make sure your repo contains:
- `telegram_bot.py`
- `file_store.json` (empty or existing)
- `requirements.txt` with:
