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
                       pending_task TEXT, language TEXT DEFAULT 'en')''')
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
def main_menu(lang='en'):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add('💰 Balance', '📋 Tasks', '📤 Withdraw', '👤 Profile')
    markup.add('📋 History', '🤔 FAQ', '👥 My Referrals', '🌍 Language')
    markup.add('🏆 Leaderboard', '📊 Statistics')
    return markup

def admin_menu():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add('📝 Task History', '💸 Withdraw History')
    markup.add('💰 Manage Balance', '⚙️ Set Task Price')
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
    buttons = ['💰 Balance', '📋 Tasks', '📤 Withdraw', '👤 Profile', '📋 History', '🤔 FAQ', '👥 My Referrals', '🌍 Language', '❌ Cancel', '🏠 Exit Admin', 'TRX', '✅ Account registered', '▶️ Start', '🏆 Leaderboard', '📊 Statistics', '🔙 Back', '🇺🇸 English', '🇧🇩 বাংলা']
    return text in buttons

# --- চ্যানেল ভেরিফিকেশন ---
def is_member(user_id):
    try:
        member = bot.get_chat_member(f"@{CHANNEL_USERNAME}", user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

# --- হেল্পার ফাংশন ল্যাঙ্গুয়েজ পাওয়ার জন্য ---
def get_user_lang(user_id):
    conn = sqlite3.connect('socialbux.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT language FROM users WHERE id=?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else 'en'

# --- /start ---
@bot.message_handler(commands=['start'])
def start_cmd(message):
    user_id = message.from_user.id
    ref_id = message.text.split()[1] if len(message.text.split()) > 1 else None

    lang = get_user_lang(user_id)
    texts = LANGUAGES[lang]

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
        cursor.execute("INSERT INTO users (id, first_name, username, referred_by, language) VALUES (?, ?, ?, ?, ?)", 
                       (user_id, message.from_user.first_name, message.from_user.username, ref_id, lang))
        if ref_id:
            conn.execute("UPDATE users SET ref_count = ref_count + 1 WHERE id=?", (ref_id,))
        conn.commit()
    conn.close()

    bot.send_message(user_id, texts['welcome'], reply_markup=main_menu(lang))

@bot.callback_query_handler(func=lambda call: call.data == "check_join")
def check_join_callback(call):
    user_id = call.from_user.id
    lang = get_user_lang(user_id)
    texts = LANGUAGES[lang]

    if is_member(user_id):
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=texts['channel_joined'])
        bot.send_message(user_id, texts['welcome'], reply_markup=main_menu(lang))
    else:
        bot.answer_callback_query(call.id, "You haven't joined the channel yet!", show_alert=True)

# --- ল্যাঙ্গুয়েজ চেঞ্জ ---
@bot.message_handler(func=lambda m: m.text in ['🇺🇸 English', '🇧🇩 বাংলা'])
def change_language(message):
    user_id = message.from_user.id
    new_lang = 'en' if message.text == '🇺🇸 English' else 'bn'
    conn = sqlite3.connect('socialbux.db', check_same_thread=False)
    conn.execute("UPDATE users SET language=? WHERE id=?", (new_lang, user_id))
    conn.commit()
    conn.close()
    texts = LANGUAGES[new_lang]
    bot.send_message(user_id, texts['lang_set'], reply_markup=main_menu(new_lang))

# --- Language বাটন ---
@bot.message_handler(func=lambda m: m.text == '🌍 Language')
def language_handler(message):
    lang = get_user_lang(message.from_user.id)
    texts = LANGUAGES[lang]
    bot.send_message(message.from_user.id, texts['language'], reply_markup=language_menu())

# --- লিডারবোর্ড ---
@bot.message_handler(func=lambda m: m.text == '🏆 Leaderboard')
def leaderboard(message):
    user_id = message.from_user.id
    lang = get_user_lang(user_id)
    texts = LANGUAGES[lang]

    conn = sqlite3.connect('socialbux.db', check_same_thread=False)
    rows = conn.execute("SELECT first_name, balance FROM users ORDER BY balance DESC LIMIT 10").fetchall()
    conn.close()

    text = texts['leaderboard']
    for i, (name, bal) in enumerate(rows, 1):
        text += f"{i}. {name} - ${bal:.4f}\n"
    if not rows:
        text += "No users yet."
    bot.send_message(user_id, text)

# --- স্ট্যাটিস্টিকস ---
@bot.message_handler(func=lambda m: m.text == '📊 Statistics')
def statistics(message):
    user_id = message.from_user.id
    lang = get_user_lang(user_id)
    texts = LANGUAGES[lang]

    conn = sqlite3.connect('socialbux.db', check_same_thread=False)
    total_users = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    total_earned = conn.execute("SELECT SUM(balance) FROM users").fetchone()[0] or 0
    total_withdrawn = conn.execute("SELECT SUM(amount) FROM withdraw_history WHERE status='Paid'").fetchone()[0] or 0
    conn.close()

    text = texts['stats'].format(total_users, total_earned, total_withdrawn)
    bot.send_message(user_id, text)

# --- বাকি সব তোর আগের কোডের মতোই (lang যোগ করে) ---
@bot.message_handler(commands=['admin'])
def admin_login(message):
    if message.from_user.id == ADMIN_ID:
        msg = bot.send_message(message.chat.id, "🔐 Enter Admin Password:")
        bot.register_next_step_handler(msg, verify_admin)

def verify_admin(message):
    if message.text == ADMIN_PASSWORD:
        bot.send_message(message.chat.id, "✅ Admin Panel Unlocked.", reply_markup=admin_menu())
    else:
        bot.send_message(message.chat.id, "❌ Wrong Password.")

@bot.message_handler(func=lambda message: True)
def handle_all(message):
    user_id = message.from_user.id
    text = message.text

    lang = get_user_lang(user_id)
    texts = LANGUAGES[lang]

    if text in ['❌ Cancel', '🏠 Exit Admin', '🔙 Back']:
        return bot.send_message(user_id, "🏠 Home.", reply_markup=main_menu(lang))

    if text == '👤 Profile':
        conn = sqlite3.connect('socialbux.db', check_same_thread=False)
        bal = conn.execute("SELECT balance FROM users WHERE id=?", (user_id,)).fetchone()[0]
        wd_res = conn.execute("SELECT SUM(amount) FROM withdraw_history WHERE user_id=? AND status='Paid'", (user_id,)).fetchone()[0]
        wd_total = wd_res if wd_res else 0.0
        conn.close()
        
        profile_msg = texts['profile'].format(message.from_user.first_name, bal, wd_total)
        return bot.send_message(user_id, profile_msg, parse_mode="HTML")

    elif text == '🤔 FAQ':
        faq_msg = "🤔 <b>View help at:</b>\n📄 https://telegra.ph/FAQ----CRAZY-MONEY-BUX-12-25-2"
        return bot.send_message(user_id, faq_msg, parse_mode="HTML")

    elif text == '📋 History':
        conn = sqlite3.connect('socialbux.db', check_same_thread=False)
        rows = conn.execute("SELECT details, status FROM task_history WHERE user_id=? ORDER BY id DESC LIMIT 15", (user_id,)).fetchall()
        conn.close()
        if not rows:
            return bot.send_message(user_id, texts['history_empty'])
        history_txt = texts['history_header']
        for r in rows:
            details, status = r
            try:
                gmail = details.split('|')[2].split(': ')[1]
                stat_emoji = "✅" if status == "Approved" else "❌" if status == "Rejected" else "⏳"
                history_txt += f"📧 {gmail}\n📊 Status: {status} {stat_emoji}\n\n"
            except: continue
        return bot.send_message(user_id, history_txt, parse_mode="HTML")

    elif text == '💰 Balance':
        conn = sqlite3.connect('socialbux.db', check_same_thread=False)
        bal = conn.execute("SELECT balance FROM users WHERE id=?", (user_id,)).fetchone()[0]
        conn.close()
        bot.send_message(user_id, texts['balance'].format(bal))

    elif text == '📋 Tasks':
        p = get_task_price()
        m = types.ReplyKeyboardMarkup(resize_keyboard=True).row(f'📱 G account (FAST CHECK) (${p:.4f})').row('❌ Cancel')
        bot.send_message(user_id, texts['tasks'], reply_markup=m)

    elif '📱 G account' in text:
        m = types.ReplyKeyboardMarkup(resize_keyboard=True).add('▶️ Start').add('❌ Cancel')
        bot.send_message(user_id, texts['task_desc'], reply_markup=m)

    elif text == '▶️ Start':
        fn, ln, p, e, rec = generate_full_creds()
        pending_data = f"FN: {fn}|LN: {ln}|E: {e}|P: {p}|REC: {rec}"
        conn = sqlite3.connect('socialbux.db', check_same_thread=False)
        conn.execute("UPDATE users SET pending_task=? WHERE id=?", (pending_data, user_id))
        conn.commit(); conn.close()
        main_msg = f"First name: <code>{fn}</code>\nLast name: <code>{ln}</code>\nPassword: <code>{p}</code>\nEmail: <code>{e}</code>\nRecovery email: <code>{rec}</code>\n\n⚠️ IMPORTANT: MANDATORY add this recovery email to account settings after registration!"
        bot.send_message(user_id, main_msg, parse_mode="HTML")
        m = types.ReplyKeyboardMarkup(resize_keyboard=True).add('✅ Account registered').add('❌ Cancel')
        bot.send_message(user_id, texts['start_task'], reply_markup=m)

    elif text == '✅ Account registered':
        try:
            price = get_task_price()
            fn_user = message.from_user.first_name
            u_name = f"@{message.from_user.username}" if message.from_user.username else "N/A"
            conn = sqlite3.connect('socialbux.db', check_same_thread=False); cursor = conn.cursor()
            res = cursor.execute("SELECT pending_task FROM users WHERE id=?", (user_id,)).fetchone()
            if res and res[0]:
                creds = res[0]
                parts = creds.split('|')
                gmail = parts[2].split(': ')[1]
                password = parts[3].split(': ')[1]
                recovery = parts[4].split(': ')[1]
                date_n = datetime.now().strftime("%Y-%m-%d %H:%M")
                cursor.execute("INSERT INTO task_history (user_id, details, status, date, amount) VALUES (?, ?, 'Pending', ?, ?)", (user_id, creds, date_n, price))
                tid = cursor.lastrowid
                conn.commit(); conn.close()
                bot.send_message(user_id, texts['submitted'], reply_markup=main_menu(lang))
                admin_msg = f"🔔 <b>New Task Submission</b>\n\n👤 <b>User ID:</b> <code>{user_id}</code>\n👤 <b>Name:</b> {fn_user}\n👤 <b>Username:</b> {u_name}\n\n      🔰<b>Task Information</b>🔰\n\n📧 <b>Gmail:</b> <code>{gmail}</code>\n🔑 <b>Pass:</b> <code>{password}</code>\n🔄 <b>Recovery:</b> <code>{recovery}</code>"
                adm_m = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("Approve", callback_data=f"app_{user_id}_{tid}"), types.InlineKeyboardButton("Reject", callback_data=f"rej_{user_id}_{tid}"))
                bot.send_message(ADMIN_ID, admin_msg, parse_mode="HTML", reply_markup=adm_m)
        except: bot.send_message(user_id, "❌ Error.")

    elif text == '👥 My Referrals':
        conn = sqlite3.connect('socialbux.db', check_same_thread=False)
        res = conn.execute("SELECT ref_count, total_ref_earn FROM users WHERE id=?", (user_id,)).fetchone()
        conn.close()
        r_link = f"https://t.me/{bot.get_me().username}?start={user_id}"
        bot.send_message(user_id, texts['referrals'].format(res[0], res[1], r_link))

    elif text == '📤 Withdraw':
        m = types.ReplyKeyboardMarkup(resize_keyboard=True).add('TRX').add('❌ Cancel')
        bot.send_message(user_id, texts['withdraw'], reply_markup=m)

    elif text == 'TRX':
        msg = bot.send_message(user_id, texts['enter_amount'])
        bot.register_next_step_handler(msg, process_withdraw_amount)

    elif user_id == ADMIN_ID:
        if text == '📝 Task History':
            conn = sqlite3.connect('socialbux.db', check_same_thread=False)
            query = "SELECT task_history.id, task_history.user_id, task_history.details, users.first_name, users.username FROM task_history JOIN users ON task_history.user_id = users.id WHERE task_history.status = 'Pending' LIMIT 10"
            rows = conn.execute(query).fetchall()
            conn.close()
            if not rows:
                bot.send_message(ADMIN_ID, texts['no_pending_tasks'])
                return
            for r in rows:
                try:
                    tid, uid, details, name, uname = r
                    parts = details.split('|')
                    gmail, password, recovery = parts[2].split(': ')[1], parts[3].split(': ')[1], parts[4].split(': ')[1]
                    hist_msg = f"🔔 <b>New Task Submission</b>\n\n👤 <b>User ID:</b> <code>{uid}</code>\n👤 <b>Name:</b> {name}\n\n      🔰<b>Task Information</b>🔰\n\n📧 <b>Gmail:</b> <code>{gmail}</code>\n🔑 <b>Pass:</b> <code>{password}</code>\n🔄 <b>Recovery:</b> <code>{recovery}</code>"
                    markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("Approve", callback_data=f"app_{uid}_{tid}"), types.InlineKeyboardButton("Reject", callback_data=f"rej_{uid}_{tid}"))
                    bot.send_message(ADMIN_ID, hist_msg, parse_mode="HTML", reply_markup=markup)
                except: continue
        
        elif text == '💸 Withdraw History':
            conn = sqlite3.connect('socialbux.db', check_same_thread=False)
            query = "SELECT w.id, w.user_id, w.amount, w.address, u.username, u.first_name FROM withdraw_history w JOIN users u ON w.user_id = u.id WHERE w.status = 'Pending'"
            rows = conn.execute(query).fetchall()
            conn.close()
            
            if not rows:
                bot.send_message(ADMIN_ID, texts['no_pending_withdraw'])
                return

            for row in rows:
                wid, uid, amount, address, username, firstname = row
                uname = f"@{username}" if username else "N/A"
                
                msg_text = f"💸 <b>Withdraw Request</b>\n\n" \
                           f"👤 <b>User:</b> {firstname} ({uname})\n" \
                           f"🆔 <b>ID:</b> <code>{uid}</code>\n" \
                           f"💰 <b>Amount:</b> ${amount}\n" \
                           f"🏦 <b>Method:</b> TRX\n" \
                           f"📫 <b>Address:</b> <code>{address}</code>"
                
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton("✅ Approve", callback_data=f"wapp_{uid}_{wid}"),
                           types.InlineKeyboardButton("❌ Reject", callback_data=f"wrej_{uid}_{wid}"))
                bot.send_message(ADMIN_ID, msg_text, parse_mode="HTML", reply_markup=markup)

        elif text == '⚙️ Set Task Price':
            msg = bot.send_message(ADMIN_ID, "🔢 Enter new task price (e.g., 0.15):")
            bot.register_next_step_handler(msg, admin_set_price_step)

        elif text == '💰 Manage Balance':
            msg = bot.send_message(ADMIN_ID, "Enter User ID:")
            bot.register_next_step_handler(msg, admin_balance_id_step)

# --- সাব ফাংশন ---
def process_withdraw_amount(message):
    user_id = message.from_user.id
    lang = get_user_lang(user_id)
    texts = LANGUAGES[lang]
    if is_menu_button(message.text): return handle_all(message)
    try:
        amount = float(message.text)
        conn = sqlite3.connect('socialbux.db', check_same_thread=False)
        bal = conn.execute("SELECT balance FROM users WHERE id=?", (user_id,)).fetchone()[0]
        conn.close()
        if bal < amount:
            bot.send_message(user_id, texts['insufficient'])
            return
        msg = bot.send_message(user_id, texts['enter_address'])
        bot.register_next_step_handler(msg, lambda m: process_withdraw_address(m, amount))
    except: bot.send_message(user_id, "⚠️ Invalid amount.")

def process_withdraw_address(message, amount):
    user_id = message.from_user.id
    lang = get_user_lang(user_id)
    texts = LANGUAGES[lang]
    if is_menu_button(message.text): return handle_all(message)
    address = message.text
    date_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    conn = sqlite3.connect('socialbux.db', check_same_thread=False)
    conn.execute("UPDATE users SET balance = balance - ? WHERE id=?", (amount, user_id))
    conn.execute("INSERT INTO withdraw_history (user_id, amount, method, address, date, status) VALUES (?, ?, 'TRX', ?, ?, 'Pending')", (user_id, amount, address, date_now))
    conn.commit(); conn.close()
    
    try:
        bot.send_message(ADMIN_ID, f"🔔 New Withdraw Request from ID: {user_id}\nAmount: ${amount}")
    except: pass
    
    bot.send_message(user_id, texts['withdrawn'], reply_markup=main_menu(lang))

def admin_balance_id_step(message):
    t_id = message.text
    msg = bot.send_message(ADMIN_ID, "Enter Amount:")
    bot.register_next_step_handler(msg, lambda m: admin_balance_save_step(m, t_id))

def admin_balance_save_step(message, t_id):
    try:
        amt = float(message.text)
        conn = sqlite3.connect('socialbux.db', check_same_thread=False); conn.execute("UPDATE users SET balance = balance + ? WHERE id=?", (amt, t_id)); conn.commit(); conn.close()
        bot.send_message(ADMIN_ID, "✅ Success.")
    except: bot.send_message(ADMIN_ID, "Error.")

def admin_set_price_step(message):
    try:
        new_price = float(message.text)
        conn = sqlite3.connect('socialbux.db', check_same_thread=False)
        conn.execute("INSERT OR REPLACE INTO settings (key, value) VALUES ('task_price', ?)", (new_price,))
        conn.commit()
        conn.close()
        bot.send_message(ADMIN_ID, f"✅ Task price updated to ${new_price:.4f}", reply_markup=admin_menu())
    except ValueError:
        bot.send_message(ADMIN_ID, "❌ Invalid number. Please enter a valid amount.", reply_markup=admin_menu())

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    try:
        data = call.data.split('_')
        act, uid, tid = data[0], data[1], data[2]
        conn = sqlite3.connect('socialbux.db', check_same_thread=False); cursor = conn.cursor()
        
        if act == 'app':
            cursor.execute("SELECT amount FROM task_history WHERE id=?", (tid,))
            res = cursor.fetchone()
            if res:
                amt = res[0]
                cursor.execute("UPDATE users SET balance = balance + ? WHERE id=?", (amt, uid))
                cursor.execute("UPDATE task_history SET status='Approved' WHERE id=?", (tid,))
                cursor.execute("SELECT referred_by FROM users WHERE id=?", (uid,))
                ref_row = cursor.fetchone()
                if ref_row and ref_row[0]:
                    ref = ref_row[0]
                    cursor.execute("UPDATE users SET balance = balance + ?, total_ref_earn = total_ref_earn + ? WHERE id=?", (amt*0.2, amt*0.2, ref))
                conn.commit()
                bot.send_message(uid, f"✅ Task Approved! ${amt} added.")
                bot.edit_message_text(f"✅ Approved Task for User {uid}", call.message.chat.id, call.message.message_id)
        
        elif act == 'rej':
            cursor.execute("UPDATE task_history SET status='Rejected' WHERE id=?", (tid,))
            conn.commit()
            bot.send_message(uid, "❌ Task Rejected.")
            bot.edit_message_text(f"❌ Rejected Task for User {uid}", call.message.chat.id, call.message.message_id)

        elif act == 'wapp':
            cursor.execute("UPDATE withdraw_history SET status='Paid' WHERE id=?", (tid,))
            conn.commit()
            bot.send_message(uid, "✅ Your withdrawal has been paid!")
            bot.edit_message_text(f"✅ Withdraw Paid for User {uid}", call.message.chat.id, call.message.message_id)
        
        elif act == 'wrej':
            cursor.execute("SELECT amount FROM withdraw_history WHERE id=?", (tid,))
            row = cursor.fetchone()
            if row:
                amt = row[0]
                cursor.execute("UPDATE users SET balance = balance + ? WHERE id=?", (amt, uid))
                cursor.execute("UPDATE withdraw_history SET status='Rejected' WHERE id=?", (tid,))
                conn.commit()
                bot.send_message(uid, f"❌ Withdrawal Rejected. ${amt} refunded to balance.")
                bot.edit_message_text(f"❌ Withdraw Rejected for User {uid}", call.message.chat.id, call.message.message_id)

        conn.close()
    except Exception as e:
        print("Error in callback:", e)

print("🤖 Crazy Money Bux Bot is Running with New Features!")

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
