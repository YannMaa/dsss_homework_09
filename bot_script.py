from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Define your bot token (from BotFather)
API_TOKEN = '7797685365:AAGT4cLNPC-0cEWBFhHwARgGJBCef6W5Jew'

# Function to handle start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hello! I am your bot. Send me a message!')

# Function to handle user messages
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Reply with the same message
    user_message = update.message.text
    print(f"Message from user: {user_message}")  # Prints to your PC/console
    await update.message.reply_text(f"Hi. What's up :)")

# Main function to set up the bot
def main() -> None:
    # Create the application object
    application = Application.builder().token(API_TOKEN).build()

    # Add command and message handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
