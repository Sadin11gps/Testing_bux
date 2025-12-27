# -*- coding: utf-8 -*-
from flask import Flask, request, abort
import telebot
from telebot import types
import sqlite3
import random
import string
from datetime import datetime
import os

# --- কনফিগ ---
API_TOKEN = os.getenv('BOT_TOKEN', '8576119064:AAE5NkXGHRQCq1iPAM5muiU1oh_5KFJGENk')
ADMIN_ID = 7702378694
ADMIN_PASSWORD = "Rdsvai11"
CHANNEL_USERNAME = "amrrdsteam"

bot = telebot.TeleBot(API_TOKEN)

app = Flask(__name__)

# --- ল্যাঙ্গুয়েজ ---
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
        # আগের মতোই বাংলা টেক্সট
        # (স্পেসের জন্য বাদ দিলাম, তোর আগের কোড থেকে কপি কর)
    }
}

# --- ডাটাবেস ---
def init_db():
    # আগের মতোই, blocked কলাম সহ

init_db()

# --- মেনু ---
def main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add('💰 Balance', '📋 Tasks')
    markup.add('📤 Withdraw', '👤 Profile')
    markup.add('📋 History', '🤔 FAQ')
    markup.add('👥 My Referrals', '🌍 Language')
    markup.add('🏆 Leaderboard', '📊 Statistics')
    return markup

# --- হ্যান্ডলার ---
@bot.message_handler(commands=['start'])
def start_cmd(message):
    # আগের মতোই, ব্লক চেক সহ

@bot.message_handler(func=lambda m: True)
def handle_all(message):
    user_id = message.from_user.id
    text = message.text

    lang = get_user_lang(user_id)
    texts = LANGUAGES[lang]

    if text == '💰 Balance':
        # ব্যালেন্স কোড
        bot.send_message(user_id, texts['balance'].format(bal))
        return

    if text == '📋 Tasks':
        # টাস্ক কোড
        bot.send_message(user_id, texts['tasks'], reply_markup=task_markup)
        return

    if text == '📤 Withdraw':
        # উইথড্র কোড
        bot.send_message(user_id, texts['withdraw'], reply_markup=withdraw_markup)
        return

    if text == '👤 Profile':
        # প্রোফাইল কোড
        bot.send_message(user_id, profile_msg, parse_mode="HTML")
        return

    if text == '📋 History':
        # হিস্ট্রি কোড
        bot.send_message(user_id, history_txt, parse_mode="HTML")
        return

    if text == '🤔 FAQ':
        bot.send_message(user_id, faq_msg, parse_mode="HTML")
        return

    if text == '👥 My Referrals':
        # রেফারেল কোড
        bot.send_message(user_id, referrals_msg)
        return

    if text == '🌍 Language':
        bot.send_message(user_id, texts['language'], reply_markup=language_menu())
        return

    if text == '🏆 Leaderboard':
        # লিডারবোর্ড কোড
        bot.send_message(user_id, leaderboard_text)
        return

    if text == '📊 Statistics':
        # স্ট্যাটিস্টিকস কোড
        bot.send_message(user_id, stats_text)
        return

    # অ্যাডমিন বাটনগুলোর জন্য আলাদা হ্যান্ডলার আছে, তাই এখানে কিছু করার দরকার নেই

# --- অ্যাডমিন হ্যান্ডলারগুলো আলাদা @bot.message_handler দিয়ে ---

# --- webhook ---

print("Bot Running!")

# webhook routes

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
