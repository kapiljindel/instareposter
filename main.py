import logging
import requests
import nest_asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, filters

# Install nest_asyncio if it's not already installed
!pip install nest_asyncio

# Apply nest_asyncio to allow multiple event loops
nest_asyncio.apply()

# Set your bot's API Token here
API_TOKEN = "7957306404:AAECTms9am4pZVXhqaCr5ulwFNVlPfDvAEQ"

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

# Main function to start the bot
async def start_bot():
    # Set up the Application (for newer versions of python-telegram-bot)
    application = Application.builder().token(API_TOKEN).build()

    # Add the handler for the Instagram links (in groups as well as private chats)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the bot and polling
    await application.run_polling()

# Run the bot
await start_bot()
