import logging
import requests
import nest_asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, MessageHandler, filters

# Apply nest_asyncio to allow multiple event loops
nest_asyncio.apply()

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Set your bot's API Token here
API_TOKEN = "7957306404:AAECTms9am4pZVXhqaCr5ulwFNVlPfDvAEQ"
bot_url = f"https://api.telegram.org/bot{API_TOKEN}/"

# Flask app setup
app = Flask(__name__)

# Function to modify the Instagram URL (edit as per your requirement)
def modify_instagram_url(instagram_url):
    if "instagram.com" in instagram_url:
        # Example modification: Replace the domain with ddinstagram.com
        modified_url = instagram_url.replace("instagram.com", "ddinstagram.com")
        return modified_url
    else:
        return "Error: This is not a valid Instagram link."

# Function to handle incoming messages
async def handle_message(update: Update, context) -> None:
    message = update.message.text.strip()

    # Debugging prints to see the message and chat type
    print(f"Received message: {message}")
    print(f"Chat type: {update.message.chat.type}")

    # Check if the message contains an Instagram URL
    if "instagram.com" in message:
        modified_url = modify_instagram_url(message)

        # Delete the original message containing the Instagram link
        await update.message.delete()

        # In a group or supergroup, send the modified URL as a new message
        if update.message.chat.type in ['group', 'supergroup']:
            await update.message.chat.send_message(f"{modified_url}")

        # In a private chat, reply to the user with the modified link
        elif update.message.chat.type == 'private':
            await update.message.reply_text(f"{modified_url}")

    else:
        # In case the message doesn't contain an Instagram link
        if update.message.chat.type in ['group', 'supergroup']:
            await update.message.chat.send_message("Please send a valid Instagram link.")
        elif update.message.chat.type == 'private':
            await update.message.reply_text("Please send a valid Instagram link.")

# Webhook endpoint that Telegram will call with updates
@app.route(f"/{API_TOKEN}", methods=["POST"])
def webhook():
    json_str = request.get_data(as_text=True)
    update = Update.de_json(json_str, bot)
    
    # Set up the application and process the update
    application = Application.builder().token(API_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Process the update
    application.update_queue.put(update)
    return "OK", 200

# Set webhook route to link your bot with Cloudflare
@app.route("/set_webhook", methods=["GET"])
def set_webhook():
    url = f"https://<your-railway-app-url>/{API_TOKEN}"
    response = requests.get(f"{bot_url}setWebhook?url={url}")
    return f"Webhook set: {response.text}"

# Main entry point to start the server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
