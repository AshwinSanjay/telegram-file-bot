import telebot
from telebot import types
import random
import string
import json
import os
from telebot.types import InputFile

# ========== CONFIG ========== #
BOT_TOKEN = '5897881599:AAGb_9BMohsAoqIRE-ioYsTmoZ1mPjqYwYA'
ADMIN_ID = 1851920719
SERVER_CHANNEL_ID = -1002521137582  # Server channel to store files
REQUIRED_CHANNEL_ID = -1001668334027  # Public channel users must join

bot = telebot.TeleBot(BOT_TOKEN)
verified_users = set()
file_links = {}
file_store = {}

# Load stored files if exist
if os.path.exists("file_store.json"):
    with open("file_store.json", "r") as f:
        file_store = json.load(f)

# ========== HELPERS ========== #
def generate_file_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

def save_file_store():
    with open("file_store.json", "w") as f:
        json.dump(file_store, f)

def check_user_joined(user_id):
    try:
        status = bot.get_chat_member(REQUIRED_CHANNEL_ID, user_id).status
        print("User status:", status)
        return status in ["creator", "administrator", "member"]
    except Exception as e:
        print("Error checking user:", e)
        return False

# ========== HANDLERS ========== #
@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.from_user.id
    username = message.from_user.first_name

    if len(message.text.split()) > 1:
        file_id = message.text.split()[1]
        if file_id in file_store:
            if user_id in verified_users or check_user_joined(user_id):
                verified_users.add(user_id)
                file_info = file_store[file_id]
                bot.send_message(user_id, f"✅ Hello {username}! Here is your file:")
                bot.send_document(user_id, file_info['file_id'])
            else:
                show_join_buttons(user_id)
        else:
            bot.send_message(user_id, "❌ Invalid file link.")
    else:
        if user_id in verified_users or check_user_joined(user_id):
            verified_users.add(user_id)
            bot.send_message(user_id, f"👋 Welcome back, {username}! You're already verified.")
        else:
            show_join_buttons(user_id)

def show_join_buttons(user_id):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔗 Join Channel", url="https://t.me/Movies_World_02"))
    markup.add(types.InlineKeyboardButton("✅ I've Joined", callback_data="verify_join"))
    bot.send_message(user_id, "🔒 To access the file, you must join our channel.", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "verify_join")
def verify_join(call):
    user_id = call.from_user.id
    if check_user_joined(user_id):
        verified_users.add(user_id)
        bot.answer_callback_query(call.id, "✅ Verified! Please click the file link again.")
        bot.send_message(user_id, "✅ You're now verified. Click the file link again to receive it.")
    else:
        bot.answer_callback_query(call.id, "❌ You're not joined yet.", show_alert=True)

@bot.message_handler(content_types=['document', 'video', 'audio', 'photo'])
def handle_files(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ You are not authorized to upload files.")
        return

    sent_msg = None
    try:
        if message.content_type == 'photo':
            file_id = message.photo[-1].file_id
            sent_msg = bot.send_photo(SERVER_CHANNEL_ID, file_id)
        elif message.content_type == 'document':
            file_id = message.document.file_id
            sent_msg = bot.send_document(SERVER_CHANNEL_ID, file_id)
        elif message.content_type == 'video':
            file_id = message.video.file_id
            sent_msg = bot.send_video(SERVER_CHANNEL_ID, file_id)
        elif message.content_type == 'audio':
            file_id = message.audio.file_id
            sent_msg = bot.send_audio(SERVER_CHANNEL_ID, file_id)

        unique_id = generate_file_id()
        file_store[unique_id] = {'file_id': file_id}
        save_file_store()

        bot.send_message(ADMIN_ID, f"✅ File uploaded successfully! Share this link:\nhttps://t.me/{bot.get_me().username}?start={unique_id}")
    except Exception as e:
        print(e)
        bot.send_message(ADMIN_ID, f"❌ Upload failed: {e}")

print("🤖 Bot is running...")
bot.polling(none_stop=True)
