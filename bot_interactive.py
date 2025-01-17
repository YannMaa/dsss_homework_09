import logging
import torch
from transformers import pipeline
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Logging for debugging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# load model Tiny Llama
print("Lade Modell...")
pipe = pipeline(
    "text-generation",
    model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    torch_dtype=torch.bfloat16,
    device_map="auto",
)
print("Modell geladen.")

# function for /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hallo! Ich bin dein Chatbot. Frag mich alles über Tiere oder andere Themen!")

#function for processing the messegas of the user
async def respond(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # read message
    user_message = update.message.text
    logger.info(f"Vollständiges Update: {update}")
    logger.info(f"Empfangene Nachricht von Benutzer: {user_message}")

    if not user_message:
        await update.message.reply_text("Entschuldigung, ich habe keine Nachricht verstanden.")
        return

    # create prompt for model
    messages = [
        {"role": "system", "content": "You are a friendly chatbot who is an expert on animals."},
        {"role": "user", "content": user_message},
    ]
    prompt = pipe.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)


    # generate answer
    try:
        outputs = pipe(prompt, max_new_tokens=100, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)
        bot_response = outputs[0]["generated_text"]
        if "<|assistant|>" in bot_response:
            bot_response = bot_response.split("<|assistant|>")[-1]  # only text after assistant
            bot_response = bot_response.replace("</s>", "").strip()  # clean answer
        else:
            bot_response = bot_response.strip()  # Fallback, if token is missing
    except Exception as e:
        bot_response = f"Entschuldigung, ich konnte gerade nicht antworten: {str(e)}"

    logger.info(f"Generierte Antwort: {bot_response}")
    await update.message.reply_text(bot_response)


# start bot
def main():
    # Token of telegram bot
    bot_token = "7797685365:AAGT4cLNPC-0cEWBFhHwARgGJBCef6W5Jew"

    # create telegram application
    application = Application.builder().token(bot_token).build()

    # register handler
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, respond))

    print("Bot läuft...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)  # polling contieunisouly

if __name__ == "__main__":
    main()
