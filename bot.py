import os
import asyncio
from dotenv import load_dotenv
from telethon import TelegramClient
import google.generativeai as genai
from util import *

load_dotenv()


async def get_channel_id(client, channel_name):
    async for dialog in client.iter_dialogs():
        if dialog.name == channel_name:
            return dialog.id


async def retrieve_todays_messages(client, channel_id):
    messages = []
    async for message in client.iter_messages(channel_id):
        message_date_israel = message.date.astimezone(israel_timezone).date()
        if message_date_israel == today_israel:
            messages.append(message)
        else:
            break

    logger.info(f"{len(messages)} messages sent today.")
    return messages


async def summarize(messages):
    google_api_key = os.environ.get('GOOGLE_API_KEY')

    if google_api_key is None:
        logger.error("Google API Key not found.")
        raise ValueError(
            "Google API Key not found in .env file. Please set the 'GOOGLE_API_KEY' environment variable."
        )

    logger.debug("Google API Key found.")

    genai.configure(api_key=google_api_key)
    model = genai.GenerativeModel(model_name='gemini-1.5-pro-latest',
                                  system_instruction=get_system_prompt())

    summary_prompt = f"הנה ההודעות שנשלחו בערוץ הטלגרם של עמית סגל ב-{today_israel}:\n\n" + '-' * 20 + '\n'

    for message in messages[::-1]:
        summary_prompt += message.text + '\n' + '-' * 20 + '\n'

    summary_prompt += "\nאנא צור סיכום תמציתי ומעניין של ההודעות הללו, בהתאם להנחיות שקיבלת."
    logger.debug(f"Summary prompt: {summary_prompt}")

    logger.info("Generating summary using Google Generative AI model.")
    try:
        response = model.generate_content(summary_prompt)
        summary = response.text
        logger.info("Summary generated successfully.")
        logger.debug(f"Summary result: {summary}")
    except Exception as e:
        logger.error(f"Summary generation failed: {e}")
        raise RuntimeError(
            "Summary generation failed. Check the logs for more details."
        ) from e

    summary_header = f"**עמית סגל - סיכום יומי | {today_israel}**\n\n"
    summary_footer = """\n\n**⚠️ שימו לב: הסיכום נערך על ידי AI ועשוי לכלול אי-דיוקים.
להודעות המקוריות, מוזמנים להיכנס לערוץ של עמית סגל: @amitsegal.
עם ישראל חי! לילה טוב 🇮🇱😴**"""

    return summary_header + summary + summary_footer


async def send_summary(client, destination_channel_id, summarized_message):
    # Send the summarized message to the destination channel
    await client.send_message(destination_channel_id, summarized_message)
    logger.info("Summarized message sent to destination channel.")


async def main():
    # Log program initiation
    logger.info("Bot initiated.")

    # Initiate relevant consts with appropriate values
    api_id = os.environ.get('TELEGRAM_API_ID')
    api_hash = os.environ.get('TELEGRAM_API_HASH')

    # Create a TelegramClient instance
    client = TelegramClient('mysession', api_id, api_hash)
    await client.start(os.environ.get('PHONE_NUMBER'))
    logger.info("Telegram client started successfully.")

    # Define source and destination's channel id's
    source_channel_id = SRC_CHANNEL_ID
    destination_channel_id = DST_CHANNEL_ID

    # Get all messages sent today from the source channel
    messages = await retrieve_todays_messages(client, source_channel_id)

    # Summarize the messages
    summarized_message = await summarize(messages)

    # Send the summarized message to the destination channel
    await send_summary(client, destination_channel_id, summarized_message)

    # Remember to stop the client
    await client.disconnect()
    logger.info("Telegram client disconnected.")


if __name__ == "__main__":
    asyncio.run(main())
