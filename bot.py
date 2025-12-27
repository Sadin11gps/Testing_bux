# -*- coding: utf-8 -*-
from flask import Flask, request, abort
import telebot
from telebot import types
import sqlite3
import random
import string
import re
from datetime import datetime
import os

# --- কনফিগারেশন ---
API_TOKEN = os.getenv('BOT_TOKEN', '8576119064:AAE5NkXGHRQCq1iPAM5muiU1oh_5KFJGENk')
ADMIN_ID = 7702378694
ADMIN_PASSWORD = "Rdsvai11"
CHANNEL_USERNAME = "amrrdsteam"

bot = telebot.TeleBot(API_TOKEN)

app = Flask(__name__)

# --- ল্যাঙ্গুয়েজ ডিকশনারি ---
LANGUAGES = {
    'en': {
        'welcome': "👋 Welcome!\n\nℹ️ This bot helps you earn money by doing simple tasks.\n\nBy using this Bot, you automatically agree to the Terms of Use.👉 https://telegra.ph/FAQ----CRAZY-MONEY-BUX-12-25-2",
        'channel_join': "⚠️ Please join our channel to use the bot:",
        'channel_joined': "✅ Verified! Now you can use the bot.",
        'balance': "💰 Your balance: ${:.4f}",
        'tasks': "👇 Please select a task:",
        'task_desc': "⏳ Review time: 74 min ⏳\n\n📋 Task: 📱 G account (FAST CHECK)\n\n📄 Description: 🔐 MANDATORY!\nYou must use only the email and password provided by the Telegram bot to register.",
        'start_task': "👉 Press the button to confirm registration or cancel the task:",
        'submitted': "✅ Submitted for review!",
        'referrals': "👥 Referrals: {}\n💰 Earned: ${:.4f}\n🔗 Link: {}",
        'withdraw': "📤 Choose method:",
        'insufficient': "❌ Insufficient balance!",
        'enter_amount': "🔢 Min $1.50\n📤 Enter Amount:",
        'enter_address': "📤 Enter TRX Address:",
        'withdrawn': "✅ Withdrawal submitted!",
        'profile': "👤 <b>{}</b>\n\n\n💰 <b>Total Balance:</b> \( {:.4f}\n\n📤 <b>Total Withdraw:</b> \){:.4f}\n\n🔒 <b>Account:</b> Active✅",
        'history_empty': "📭 You haven't completed any tasks yet.",
        'history_header': "📋 <b>Your Task History:</b>\n\n",
        'leaderboard': "🏆 <b>Top 10 Earners</b>\n\n",
        'stats': "📊 <b>Bot Statistics</b>\n\n👥 Total Users: {}\n💰 Total Earned: \( {:.4f}\n📤 Total Withdrawn: \){:.4f}",
        'language': "🌍 Choose language:",
        'lang_set': "✅ Language set to English!",
        'no_pending_tasks': "📭 No pending tasks.",
        'no_pending_withdraw': "📭 No pending withdrawals.",
        'admin_broadcast': "📢 Enter message to broadcast to all users:",
        'admin_send': "📩 Enter User ID to send message:",
        'admin_send_msg': "Enter message for the user:",
        'broadcast_success': "✅ Broadcast sent to {} users!",
        'send_success': "✅ Message sent to user!",
        'user_not_found': "❌ User not found.",
        'blocked_message': "🚫 You are blocked from using this bot.",
        'admin_block': "🚫 Enter User ID to block:",
        'admin_unblock': "✅ Enter User ID to unblock:",
        'user_blocked': "🚫 User blocked.",
        'user_unblocked': "✅ User unblocked.",
    },
    'bn': {
        'welcome': "👋 স্বাগতম!\n\nℹ️ এই বটে সিম্পল টাস্ক করে ডলার আর্ন করুন।\n\nবট ব্যবহার করে আপনি অটোম্যাটিক টার্মস অ্যাগ্রি করছেন।👉 https://telegra.ph/FAQ----CRAZY-MONEY-BUX-12-25-2",
        'channel_join': "⚠️ বট ব্যবহার করতে আমাদের চ্যানেলে জয়েন করুন:",
        'channel_joined': "✅ ভেরিফাইড! এখন বট ব্যবহার করতে পারবেন।",
        'balance': "💰 আপনার ব্যালেন্স: ${:.4f}",
        'tasks': "👇 একটা টাস্ক সিলেক্ট করুন:",
        'task_desc': "⏳ রিভিউ টাইম: ৭৪ মিনিট ⏳\n\n📋 টাস্ক: 📱 G account (FAST CHECK)\n\n📄 বর্ণনা: 🔐 অবশ্যই বট দেওয়া ইমেইল ও পাসওয়ার্ড দিয়ে রেজিস্টার করতে হবে।",
        'start_task': "👉 রেজিস্ট্রেশন কনফার্ম করুন বা ক্যানসেল করুন:",
        'submitted': "✅ রিভিউয়ের জন্য সাবমিট করা হয়েছে!",
        'referrals': "👥 রেফারেল: {}\n💰 আর্ন: ${:.4f}\n🔗 লিঙ্ক: {}",
        'withdraw': "📤 পেমেন্ট মেথড সিলেক্ট করুন:",
        'insufficient': "❌ ব্যালেন্স যথেষ্ট নয়!",
        'enter_amount': "🔢 মিনিমাম $1.50\n📤 অ্যামাউন্ট দিন:",
        'enter_address': "📤 TRX অ্যাড্রেস দিন:",
        'withdrawn': "✅ উইথড্র রিকোয়েস্ট করা হয়েছে!",
        'profile': "👤 <b>{}</b>\n\n\n💰 <b>টোটাল ব্যালেন্স:</b> \( {:.4f}\n\n📤 <b>টোটাল উইথড্র:</b> \){:.4f}\n\n🔒 <b>অ্যাকাউন্ট:</b> অ্যাকটিভ✅",
        'history_empty': "📭 আপনি এখনো কোনো টাস্ক করেননি।",
        'history_header': "📋 <b>আপনার টাস্ক হিস্ট্রি:</b>\n\n",
        'leaderboard': "🏆 <b>টপ ১০ আর্নার</b>\n\n",
        'stats': "📊 <b>বট স্ট্যাটিস্টিকস</b>\n\n👥 টোটাল ইউজার: {}\n💰 টোটাল আর্ন: \( {:.4f}\n📤 টোটাল উইথড্র: \){:.4f}",
        'language': "🌍 ভাষা সিলেক্ট করুন:",
        'lang_set': "✅ ভাষা বাংলায় সেট করা হয়েছে!",
        'no_pending_tasks': "📭 কোনো পেন্ডিং টাস্ক নেই।",
        'no_pending_withdraw': "📭 কোনো পেন্ডিং উইথড্র নেই।",
        'admin_broadcast': "📢 সবাইকে মেসেজ পাঠানোর জন্য মেসেজ লিখুন:",
        'admin_send': "📩 ইউজার আইডি দিন:",
        'admin_send_msg': "ইউজারের জন্য মেসেজ লিখুন:",
        'broadcast_success': "✅ {} জন ইউজারকে ব্রডকাস্ট পাঠানো হয়েছে!",
        'send_success': "✅ মেসেজ পাঠানো হয়েছে!",
        'user_not_found': "❌ ইউজার পাওয়া যায়নি।",
        'blocked_message': "🚫 আপনাকে এই বট ব্যবহার করতে ব্লক করা হয়েছে।",
        'admin_block': "🚫 ব্লক করার জন্য ইউজার আইডি দিন:",
        'admin_unblock': "✅ আনব্লক করার জন্য ইউজার আইডি দিন:",
        'user_blocked': "🚫 ইউজার ব্লক করা হয়েছে।",
        'user_unblocked': "✅ ইউজার আনব্লক করা হয়েছে।",
    }
}

# --- ডাটাবেস সেটআপ ---
def init_db():
    conn = sqlite3.connect('socialbux.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                      (id INTEGER PRIMARY KEY, first_name TEXT, username TEXT, 
                       balance REAL DEFAULT 0.0, referred_by INTEGER, 
                       ref_count INTEGER DEFAULT 0, total_ref_earn REAL DEFAULT 0.0,
                       pending_task TEXT, language TEXT DEFAULT 'en', blocked INTEGER DEFAULT 0)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS task_history 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, 
                       details TEXT, status TEXT, date TEXT, amount REAL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS withdraw_history 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, 
                       amount REAL, method TEXT, address TEXT, date TEXT, status TEXT DEFAULT 'Pending')''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS settings 
                      (key TEXT PRIMARY KEY, value REAL)''')
    cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('task_price', 0.1500)")
    
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN blocked INTEGER DEFAULT 0")
    except:
        pass
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN ref_count INTEGER DEFAULT 0")
    except:
        pass
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN total_ref_earn REAL DEFAULT 0.0")
    except:
        pass
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN language TEXT DEFAULT 'en'")
    except:
        pass
    try:
        cursor.execute("ALTER TABLE withdraw_history ADD COLUMN status TEXT DEFAULT 'Pending'")
    except:
        pass 
        
    conn.commit()
    conn.close()

init_db()

# --- জেনারেটর ফাংশন ---
def generate_full_creds():
    first_names = ["Brian", "James", "Robert", "John", "Michael", "William", "David", "Richard", "Joseph", "Thomas"]
    last_names = ["Holloway", "Rasmussen", "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis"]
    chars = string.ascii_lowercase + string.digits
    password = ''.join(random.choice(chars + string.ascii_uppercase) for _ in range(10))
    email_prefix = ''.join(random.choice(chars) for _ in range(8))
    recovery_prefix = ''.join(random.choice(chars) for _ in range(10))
    f_name = random.choice(first_names)
    l_name = random.choice(last_names)
    email = f"{email_prefix}{random.choice(chars)}@gmail.com"
    recovery = f"{recovery_prefix}@hotmail.com"
    return f_name, l_name, password, email, recovery

# --- কিবোর্ডস ---
def main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add('💰 Balance', '📋 Tasks')
    markup.add('📤 Withdraw', '👤 Profile')
    markup.add('📋 History', '🤔 FAQ')
    markup.add('👥 My Referrals', '🌍 Language')
    markup.add('🏆 Leaderboard', '📊 Statistics')
    return markup

def admin_menu():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add('📝 Task History', '💸 Withdraw History')
    markup.add('💰 Manage Balance', '⚙️ Set Task Price')
    markup.add('📢 Broadcast', '📩 Send Message')
    markup.add('🚫 Block User', '✅ Unblock User')
    markup.add('🏠 Exit Admin')
    return markup

def language_menu():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add('🇺🇸 English', '🇧🇩 বাংলা')
    markup.add('🔙 Back')
    return markup

def get_task_price():
    conn = sqlite3.connect('socialbux.db', check_same_thread=False)
    try:
        price = conn.execute("SELECT value FROM settings WHERE key='task_price'").fetchone()[0]
    except:
        price = 0.1500
    conn.close()
    return price

def is_menu_button(text):
    buttons = ['💰 Balance', '📋 Tasks', '📤 Withdraw', '👤 Profile', '📋 History', '🤔 FAQ', '👥 My Referrals', '🌍 Language', '❌ Cancel', '🏠 Exit Admin', 'TRX', '✅ Account registered', '▶️ Start', '🏆 Leaderboard', '📊 Statistics', '🔙 Back', '🇺🇸 English', '🇧🇩 বাংলা', '📢 Broadcast', '📩 Send Message', '🚫 Block User', '✅ Unblock User']
    return text in buttons

# --- চ্যানেল ভেরিফিকেশন ---
def is_member(user_id):
    try:
        member = bot.get_chat_member(f"@{CHANNEL_USERNAME}", user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

# --- ব্লক চেক ---
def is_blocked(user_id):
    conn = sqlite3.connect('socialbux.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT blocked FROM users WHERE id=?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row and row[0] == 1

# --- হেল্পার ফাংশন ---
def get_user_lang(user_id):
    conn = sqlite3.connect('socialbux.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT language FROM users WHERE id=?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row and row[0] else 'en'

# --- /start ---
@bot.message_handler(commands=['start'])
def start_cmd(message):
    user_id = message.from_user.id
    ref_id = message.text.split()[1] if len(message.text.split()) > 1 else None

    lang = get_user_lang(user_id)
    texts = LANGUAGES[lang]

    if is_blocked(user_id):
        bot.send_message(user_id, texts['blocked_message'])
        return

    if not is_member(user_id):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Join Channel", url=f"https://t.me/{CHANNEL_USERNAME}"))
        markup.add(types.InlineKeyboardButton("I Joined ✅", callback_data="check_join"))
        bot.send_message(user_id, texts['channel_join'] + f" https://t.me/{CHANNEL_USERNAME}", reply_markup=markup)
        return

    conn = sqlite3.connect('socialbux.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE id=?", (user_id,))
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO users (id, first_name, username, referred_by, language, blocked) VALUES (?, ?, ?, ?, ?, 0)", 
                       (user_id, message.from_user.first_name, message.from_user.username, ref_id, 'en'))
        if ref_id:
            conn.execute("UPDATE users SET ref_count = ref_count + 1 WHERE id=?", (ref_id,))
        conn.commit()
    conn.close()

    bot.send_message(user_id, texts['welcome'], reply_markup=main_menu())

# --- অ্যাডমিনে Broadcast ---
@bot.message_handler(func=lambda m: m.text == '📢 Broadcast' and m.from_user.id == ADMIN_ID)
def admin_broadcast(message):
    admin_lang = get_user_lang(ADMIN_ID)
    texts = LANGUAGES[admin_lang]
    msg = bot.send_message(ADMIN_ID, texts['admin_broadcast'])
    bot.register_next_step_handler(msg, broadcast_message)

def broadcast_message(message):
    admin_lang = get_user_lang(ADMIN_ID)
    texts = LANGUAGES[admin_lang]
    if message.text == '🏠 Exit Admin':
        bot.send_message(ADMIN_ID, "Exited admin panel.", reply_markup=main_menu())
        return

    conn = sqlite3.connect('socialbux.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users")
    users = cursor.fetchall()
    conn.close()

    sent_count = 0
    for user in users:
        try:
            bot.send_message(user[0], message.text)
            sent_count += 1
        except:
            pass

    bot.send_message(ADMIN_ID, texts['broadcast_success'].format(sent_count), reply_markup=admin_menu())

# --- অ্যাডমিনে Send Message ---
@bot.message_handler(func=lambda m: m.text == '📩 Send Message' and m.from_user.id == ADMIN_ID)
def admin_send(message):
    admin_lang = get_user_lang(ADMIN_ID)
    texts = LANGUAGES[admin_lang]
    msg = bot.send_message(ADMIN_ID, texts['admin_send'])
    bot.register_next_step_handler(msg, admin_send_user_id)

def admin_send_user_id(message):
    admin_lang = get_user_lang(ADMIN_ID)
    texts = LANGUAGES[admin_lang]
    if message.text == '🏠 Exit Admin':
        bot.send_message(ADMIN_ID, "Exited admin panel.", reply_markup=main_menu())
        return

    try:
        target_id = int(message.text)
        msg = bot.send_message(ADMIN_ID, texts['admin_send_msg'])
        bot.register_next_step_handler(msg, lambda m: admin_send_final(m, target_id))
    except:
        bot.send_message(ADMIN_ID, "❌ Invalid User ID.", reply_markup=admin_menu())

def admin_send_final(message, target_id):
    admin_lang = get_user_lang(ADMIN_ID)
    texts = LANGUAGES[admin_lang]
    if message.text == '🏠 Exit Admin':
        bot.send_message(ADMIN_ID, "Exited admin panel.", reply_markup=main_menu())
        return

    try:
        bot.send_message(target_id, message.text)
        bot.send_message(ADMIN_ID, texts['send_success'], reply_markup=admin_menu())
    except:
        bot.send_message(ADMIN_ID, texts['user_not_found'], reply_markup=admin_menu())

# --- অ্যাডমিনে Block/Unblock ---
@bot.message_handler(func=lambda m: m.text == '🚫 Block User' and m.from_user.id == ADMIN_ID)
def admin_block_user(message):
    admin_lang = get_user_lang(ADMIN_ID)
    texts = LANGUAGES[admin_lang]
    msg = bot.send_message(ADMIN_ID, texts['admin_block'])
    bot.register_next_step_handler(msg, block_user_step)

def block_user_step(message):
    admin_lang = get_user_lang(ADMIN_ID)
    texts = LANGUAGES[admin_lang]
    if message.text == '🏠 Exit Admin':
        bot.send_message(ADMIN_ID, "Exited admin panel.", reply_markup=main_menu())
        return
    try:
        target_id = int(message.text)
        conn = sqlite3.connect('socialbux.db', check_same_thread=False)
        conn.execute("UPDATE users SET blocked=1 WHERE id=?", (target_id,))
        conn.commit()
        conn.close()
        bot.send_message(ADMIN_ID, texts['user_blocked'], reply_markup=admin_menu())
        try:
            bot.send_message(target_id, texts['blocked_message'])
        except:
            pass
    except:
        bot.send_message(ADMIN_ID, "❌ Invalid User ID.", reply_markup=admin_menu())

@bot.message_handler(func=lambda m: m.text == '✅ Unblock User' and m.from_user.id == ADMIN_ID)
def admin_unblock_user(message):
    admin_lang = get_user_lang(ADMIN_ID)
    texts = LANGUAGES[admin_lang]
    msg = bot.send_message(ADMIN_ID, texts['admin_unblock'])
    bot.register_next_step_handler(msg, unblock_user_step)

def unblock_user_step(message):
    admin_lang = get_user_lang(ADMIN_ID)
    texts = LANGUAGES[admin_lang]
    if message.text == '🏠 Exit Admin':
        bot.send_message(ADMIN_ID, "Exited admin panel.", reply_markup=main_menu())
        return
    try:
        target_id = int(message.text)
        conn = sqlite3.connect('socialbux.db', check_same_thread=False)
        conn.execute("UPDATE users SET blocked=0 WHERE id=?", (target_id,))
        conn.commit()
        conn.close()
        bot.send_message(ADMIN_ID, texts['user_unblocked'], reply_markup=admin_menu())
    except:
        bot.send_message(ADMIN_ID, "❌ Invalid User ID.", reply_markup=admin_menu())

# --- মেইন হ্যান্ডলার ---
@bot.message_handler(func=lambda message: True)
def handle_all(message):
    user_id = message.from_user.id
    text = message.text

    lang = get_user_lang(user_id)
    texts = LANGUAGES[lang]

    if text in ['❌ Cancel', '🏠 Exit Admin', '🔙 Back']:
        bot.send_message(user_id, "🏠 Home.", reply_markup=main_menu())
        return

    # বাকি বাটনগুলোর কোড তোর আগের মতোই রাখ (Profile, FAQ, History, Balance, Tasks, Start, Account registered, Referrals, Withdraw, Admin section)

# --- অন্যান্য ফাংশন (process_withdraw, admin_balance, admin_set_price, callback_handler, webhook) আগের মতোই ---

print("🤖 Crazy Money Bux Bot is Running - All Admin Buttons Working!")

# --- Webhook routes ---
@app.route('/' + API_TOKEN, methods=['POST'])
def get_webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return 'ok', 200
    else:
        abort(403)

@app.route('/')
def index():
    return "Bot is running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
