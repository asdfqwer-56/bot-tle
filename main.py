#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)
from keep_alive import keep_alive

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = "YOUR_BOT_TOKEN"
ADMINS = [123456789]
VIP_USERS = {}

# الرد الآمن
async def safe_reply(update: Update, text: str, parse_mode="Markdown", reply_markup=None):
    try:
        if update.callback_query:
            await update.callback_query.edit_message_text(
                text=text, parse_mode=parse_mode, reply_markup=reply_markup
            )
        elif update.message:
            await update.message.reply_text(
                text=text, parse_mode=parse_mode, reply_markup=reply_markup
            )
    except Exception as e:
        logger.error(f"safe_reply error: {e}")

# أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    buttons = [
        [InlineKeyboardButton("📚 الأوامر", callback_data="help_cmd")],
        [InlineKeyboardButton("🎟 VIP", callback_data="vip_info")],
        [InlineKeyboardButton("🗂 تحميل ملفات ببجي", callback_data="pubg_files")],
        [InlineKeyboardButton("👨‍💻 الدعم", url="https://t.me/username")]
    ]
    msg = f"✨ **مرحبًا {user.first_name}** ✨\n\nأهلاً بك في بوتنا! اختر من الخيارات:"
    await safe_reply(update, msg, reply_markup=InlineKeyboardMarkup(buttons))

# أمر /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    commands = "📋 **قائمة الأوامر:**\n\n/start - بدء\n/help - المساعدة\n/vip - VIP\n/admin - لوحة التحكم"
    await safe_reply(update, commands)

# VIP Info
async def vip_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    is_vip = update.effective_user.id in VIP_USERS
    msg = f"🎖 **معلومات VIP**\n\nحالتك: {'🌟 VIP' if is_vip else '🔹 عادي'}\n\nالمميزات:\n✅ دعم مميز\n✅ سرعة\n✅ ميزات خاصة"
    buttons = []
    if not is_vip:
        buttons.append([InlineKeyboardButton("💎 ترقية إلى VIP", callback_data="upgrade_vip")])
    await safe_reply(update, msg, reply_markup=InlineKeyboardMarkup(buttons) if buttons else None)

# ملفات ببجي
async def pubg_files(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "🗂 **تحميل ملفات ببجي:**\n\n- [ملف 1](https://example.com/file1)\n- [ملف 2](https://example.com/file2)\n- [ملف 3](https://example.com/file3)"
    await safe_reply(update, msg, parse_mode="Markdown", reply_markup=None)

# أزرار
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    if data == "help_cmd":
        await help_command(update, context)
    elif data == "vip_info":
        await vip_info(update, context)
    elif data == "pubg_files":
        await pubg_files(update, context)

# خطأ
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"حدث خطأ: {context.error}", exc_info=True)
    if isinstance(update, Update):
        await safe_reply(update, "⚠️ حدث خطأ. حاول لاحقًا.")

# بدء البوت
def main():
    keep_alive()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("vip", vip_info))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_error_handler(error_handler)
    app.run_polling()

if __name__ == "__main__":
    main()
