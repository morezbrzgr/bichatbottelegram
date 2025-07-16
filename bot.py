import logging
import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# فعال کردن لاگ‌ها برای دیباگ
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# دریافت توکن از متغیر محیطی
TOKEN = os.getenv("TELEGRAM_API_TOKEN")

# دیکشنری برای ذخیره لینک‌های ناشناس کاربران
user_links = {}

# دستورات ربات
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        'سلام! من ربات چت ناشناس هستم. برای شروع چت دستور /connect رو ارسال کن.'
    )

def help(update: Update, context: CallbackContext):
    update.message.reply_text(
        'دستورات من:\n'
        '/start - شروع به کار ربات\n'
        '/connect - اتصال به یک مخاطب خاص\n'
        '/link - دریافت لینک ناشناس'
    )

def connect(update: Update, context: CallbackContext):
    """اتصال به مخاطب خاص"""
    # این بخش باید برای کاربرانی که قبلاً ثبت‌نام کرده‌اند کار کند
    user_id = update.message.from_user.id
    # ذخیره لینک ناشناس برای هر کاربر
    user_link = f"https://t.me/{update.message.from_user.username}?start={user_id}"
    user_links[user_id] = user_link
    update.message.reply_text(f"برای شروع چت با یک نفر، لینک زیر رو استفاده کن:\n{user_link}")

def send_anonymous_message(update: Update, context: CallbackContext):
    """ارسال پیام به طور ناشناس"""
    user_id = update.message.from_user.id
    if user_id in user_links:
        # اینجا باید متن پیام ارسال بشه
        update.message.reply_text("پیام شما به طور ناشناس ارسال شد.")
    else:
        update.message.reply_text("ابتدا باید دستور /connect رو ارسال کنی.")

def get_link(update: Update, context: CallbackContext):
    """دریافت لینک ناشناس"""
    user_id = update.message.from_user.id
    if user_id in user_links:
        link = user_links[user_id]
        update.message.reply_text(f"لینک ناشناس شما: {link}")
    else:
        update.message.reply_text("ابتدا باید دستور /connect رو ارسال کنی.")

# هندلرهای ربات
def main():
    # ساخت Updater با توکن
    updater = Updater(TOKEN, use_context=True)

    # دریافت دیسپاچر برای اضافه کردن هندلرها
    dispatcher = updater.dispatcher

    # اضافه کردن هندلرها
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler("connect", connect))
    dispatcher.add_handler(CommandHandler("link", get_link))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, send_anonymous_message))

    # شروع ربات
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
