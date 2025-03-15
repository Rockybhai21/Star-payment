import os
import logging
from telegram import Update, LabeledPrice
from telegram.ext import Updater, CommandHandler, CallbackContext, PreCheckoutQueryHandler, MessageHandler, Filters
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
TELEGRAM_STAR_PROVIDER = "TELEGRAM_STAR_PROVIDER"

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Welcome! Use /buy_stars to purchase in-app features.")

def buy_stars(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    title = "Premium Feature"
    description = "Unlock premium bot features using Telegram Stars!"
    payload = "star_payment_payload"
    currency = "TGS"  # Telegram Stars currency
    prices = [LabeledPrice("Premium Access", 100)]  # 100 Stars

    context.bot.send_invoice(
        chat_id,
        title,
        description,
        payload,
        TELEGRAM_STAR_PROVIDER,
        currency,
        prices
    )

def precheckout_callback(update: Update, context: CallbackContext):
    query = update.pre_checkout_query
    if query.invoice_payload != "star_payment_payload":
        query.answer(ok=False, error_message="Something went wrong!")
    else:
        query.answer(ok=True)

def successful_payment_callback(update: Update, context: CallbackContext):
    update.message.reply_text("✅ Payment successful! You've unlocked premium access.")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("buy_stars", buy_stars))
    dp.add_handler(PreCheckoutQueryHandler(precheckout_callback))
    dp.add_handler(MessageHandler(Filters.successful_payment, successful_payment_callback))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
