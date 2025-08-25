from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, ContextTypes

MENU, QUANTITY, PHONE = range(3)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["🍔 Burger", "🍕 Pizza", "🥤 Cola"]]
    await update.message.reply_text(
        "Welcome! Choose a product:",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    )
    return MENU

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["product"] = update.message.text
    await update.message.reply_text("How many do you want?")
    return QUANTITY

async def quantity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["quantity"] = update.message.text
    await update.message.reply_text("Please send your phone number 📞")
    return PHONE

async def phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    phone = update.message.text
    product = context.user_data["product"]
    quantity = context.user_data["quantity"]

    await update.message.reply_text("✅ Your order has been received! We will contact you soon.")
    
    # Send order info to admin (replace with your telegram ID)
    admin_id = 123456789  
    await context.bot.send_message(
        chat_id=admin_id,
        text=f"📦 New order:\nProduct: {product}\nQuantity: {quantity}\nPhone: {phone}"
    )
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Order canceled.")
    return ConversationHandler.END

def main():
    app = Application.builder().token("YOUR_BOT_TOKEN").build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, menu)],
            QUANTITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, quantity)],
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, phone)],
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    app.add_handler(conv_handler)
    app.run_polling()

if __name__ == "__main__":
    main()
