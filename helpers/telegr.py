from decouple import config
from telegram import Bot
from models.settings import Settings
import shared_vars as sv

async def send_inform_message(telegram_token, message, image_path: str, send_pic: bool):
    try:
        api_token = config(telegram_token)
        chat_id = config("CHAT_ID")

        bot = Bot(token=api_token)

        response = None
        if send_pic:
            with open(image_path, 'rb') as photo:
                response = await bot.send_photo(chat_id=chat_id, photo=photo, caption=message)
        else:
            response = await bot.send_message(chat_id=chat_id, text=message)

        if response:
            pass
        else:
            print("Failed to send inform message.")
    except Exception as e:
        print("An error occurred:", str(e))

async def check_and_handle_message(settings: Settings):
    global old_timestamp
    try:
        # Get the necessary credentials from the configuration file
        api_token = config(settings.telegram_token)

        # Create a Telegram bot instance
        bot = Bot(token=api_token)

        # Get the latest message from the bot's chat
        updates = await bot.get_updates()
        message = ''
        if len(updates) > 0:
            message = updates[-1].message
        else: 
            return

        # Check if there is a new message
        if message is not None and old_timestamp != message.date.timestamp() and (time.time() - message.date.timestamp()) <= 30:
            old_timestamp = message.date.timestamp()
            if message.text == 'pause' or message.text == 'Pause':
                sv.pause = not sv.pause

            print("New message handled successfully!")
    except Exception as e:
        print("An error occurred:", str(e))