#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import json
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("TOKEN")
ADMINS = [123456789]
VIP_USERS = {}

# تحميل روابط ملفات ببجي
PUBG_FILE = "pubg_files.json"
if not os.path.exists(PUBG_FILE):
    with open(PUBG_FILE, "w") as f:
        json.dump({}, f)

def load_pubg_files():
    with open(PUBG_FILE, "r") as f:
        return json.load(f)

async def safe_reply(update: Update, text: str, parse_mode="Markdown", reply_markup=None):
    try:
        if update.callback_query:
            await update.callback_query.edit_message_text(
                text=text,
                parse_mode=parse_mode,
                reply_markup=reply_markup
            )
        elif update.message:
            await update.message.reply_text(
                text=text,
                parse_mode=parse_mode,
                reply_markup=reply_markup
            )
    except Exception as e:
        logger.error(f"خطأ في safe_reply: {e}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    buttons = [
        [InlineKeyboardButton("📚 الأوامر", callback_data="help_cmd")],
        [InlineKeyboardButton("🎟 VIP", callback_data="vip_info")],
        [InlineKeyboardButton("📦 ملفات ببجي", callback_data="pubg_files")],
        [InlineKeyboardButton("👨‍💻 الدعم", url="https://t.me/username")]
    ]
    welcome_msg = f"""
✨ **مرحبًا {user.first_name}** ✨

أهلاً بك في بوتنا المميز!
اختر أحد الخيارات من الأسفل:
"""
    await safe_reply(update, welcome_msg, reply_markup=InlineKeyboardMarkup(buttons))

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    commands = """
📋 **قائمة الأوامر المتاحة:**

🔹 /start - بدء استخدام البوت
🔹 /help - عرض هذه القائمة
🔹 /vip - معلومات العضوية المميزة
🔹 /admin - لوحة التحكم (للمسؤولين)
"""
    await safe_reply(update, commands)

async def vip_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    is_vip = update.effective_user.id in VIP_USERS
    vip_msg = f"""
🎖 **معلومات VIP**

حالة عضويتك: {'🌟 VIP مميز' if is_vip else '🔹 عضو عادي'}

مميزات VIP:
✅ دعم فني مميز
✅ ميزات حصرية
✅ سرعة استجابة أعلى
"""
    buttons = []
    if not is_vip:
        buttons.append([InlineKeyboardButton("💎 ترقية إلى VIP", callback_data="upgrade_vip")])

    await safe_reply(update, vip_msg, reply_markup=InlineKeyboardMarkup(buttons) if buttons else None)

async def pubg_files_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    files = load_pubg_files()
    if not files:
        return await safe_reply(update, "❌ لا توجد ملفات متاحة حالياً.")
    msg = "🎮 **ملفات ببجي المتوفرة:**
"
    for name, link in files.items():
        msg += f"
🔹 [{name}]({link})"
    await safe_reply(update, msg)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "help_cmd":
        await help_command(update, context)
    elif query.data == "vip_info":
        await vip_info(update, context)
    elif query.data == "pubg_files":
        await pubg_files_list(update, context)

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"حدث خطأ: {context.error}", exc_info=True)
    if isinstance(update, Update):
        await safe_reply(update, "⚠️ حدث خطأ ما. يرجى المحاولة لاحقًا.")

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("vip", vip_info))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_error_handler(error_handler)
    application.run_polling()

if __name__ == "__main__":
    main()
