import os
import logging
from datetime import datetime
import pytz

from dotenv import load_dotenv
from telethon import TelegramClient
import google.generativeai as genai
from util import *

load_dotenv()

# Set up logging
logger = logging.getLogger('bot')
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('bot_logs.log')
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(funcName)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

async def get_channel_id(client, channel_name):
    async for dialog in client.iter_dialogs():
        if dialog.name == channel_name:
            return dialog.id

async def get_todays_messages(client, channel_id):
    israel_timezone = pytz.timezone('Israel')
    today_israel = datetime.now(israel_timezone).date()

    messages = []
    async for message in client.iter_messages(channel_id):
        message_date_israel = message.date.astimezone(israel_timezone).date()   
        if message_date_israel == today_israel:
            messages.append(message)
        else:
            break
    
    logger.info(f"Collected {len(messages)} messages for today.")
    return messages

async def summarize(messages):
    google_api_key = os.environ.get('GOOGLE_API_KEY')

    if google_api_key is None:
        logger.error("Google API Key not found.")
        raise ValueError("Google API Key not found in .env file. Please set the 'GOOGLE_API_KEY' environment variable.")
    
    logger.debug("Google API Key found.")

    genai.configure(api_key=google_api_key)
    model = genai.GenerativeModel('gemini-pro')

    israel_timezone = pytz.timezone('Israel')
    today_israel = datetime.now(israel_timezone).date()
    prompt_text = get_base_prompt(today_israel)

    for message in messages[::-1]:
        prompt_text += message.text + '\n' + '###' + '\n'
    
    logger.debug(f"Completed prompt defenition. Prompt: {prompt_text}")

    logger.info("Generating summary using Google Generative AI model.")
    response = model.generate_content(prompt_text)
    summary_end = '''**⚠️ הסיכום נכתב על ידי בינה מלאכותית ויכול להיות לא מדויק ואף שגוי לפעמים. להודעות המקוריות מוזמנים להיכנס לערוץ של עמית סגל @amitsegal. עם ישראל חי! לילה טוב 😴**'''

    try:
        summary = response.text + 2*'\n' + summary_end
        logger.info("Summary generated successfully.")
        logger.debug(f"Summary result: {summary}")
    except Exception as e:
        logger.error(f"Summary generation failed: {e}\nResponse feedback: {response.prompt_feedback}")
        raise RuntimeError("Summary generation failed. Check the logs for more details.") from e

    return summary

async def send_summary(client, destination_channel_id, summarized_message):
    # Send the summarized message to the destination channel
    await client.send_message(destination_channel_id, summarized_message)
    logger.info("Summarized message sent to destination channel.")

async def main():
    # Log program initiation
    logger.info("Program initiated.")

    # Initiate relevant consts with appropriate values
    api_id = os.environ.get('TELEGRAM_API_ID')
    api_hash = os.environ.get('TELEGRAM_API_HASH')

    # Create a TelegramClient instance
    client = TelegramClient('mysession', api_id, api_hash)
    await client.start(os.environ.get('PHONE_NUMBER'))
    logger.info("Telegram client started successfully.")

    '''
    # To find the chatID for the first time, replace 'your_channel_name' with the name of the source channel and run this lines:
    source_channel_name = "🇮🇱 עמית סגל - סיכום יומי 🇮🇱"
    source_channel_id = await get_channel_id(client, source_channel_name)
    print("Source Channel ID:", source_channel_id)
    '''

    # Define source and destination's channel id's
    source_channel_id = SRC_CHANNEL_ID
    destination_channel_id = DST_CHANNEL_ID

    # Get all messages sent today from the source channel
    messages = await get_todays_messages(client, source_channel_id)

    # Summarize the messages
    summarized_message = await summarize(messages)

    # Send the summarized message to the destination channel
    await send_summary(client, destination_channel_id, summarized_message)

    # Remember to stop the client
    await client.disconnect()
    logger.info("Telegram client disconnected.")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
