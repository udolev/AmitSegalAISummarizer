# AmitSegalAISummarizer

A Telegram bot that summarizes Amit Segal's daily messages and posts them on a dedicated channel.

## Overview

This bot automatically retrieves messages from Amit Segal's Telegram channel, summarizes them using Google's Generative AI, and posts the summary to a specified destination channel. It's designed to run daily at 23:00 using a cron job.

## Features

- Retrieves today's messages from Amit Segal's channel
- Summarizes the content using Google's Generative AI (Gemini 1.5 Pro)
- Posts the summary to a specified Telegram channel
- Runs automatically at scheduled times
- Provides structured summaries focusing on security updates, political updates, and daily quotes

## Prerequisites

- Python 3.11+
- Poetry (for dependency management)
- Telegram API credentials
- Google Generative AI API key

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/udolev/AmitSegalAISummarizer.git
   cd AmitSegalAISummarizer
   ```

2. Install dependencies using Poetry:
   ```
   poetry install
   ```

3. Set up environment variables:
   Create a `.env` file in the project root with the following:
   ```
   TELEGRAM_API_ID=your_telegram_api_id
   TELEGRAM_API_HASH=your_telegram_api_hash
   PHONE_NUMBER=your_phone_number
   GOOGLE_API_KEY=your_google_api_key
   ```

## Project Structure

- `bot.py`: Main script containing the bot logic
- `util.py`: Utility file containing constants, logging configuration, and system prompt
- `pyproject.toml`: Poetry configuration file
- `poetry.lock`: Lock file for dependencies
- `run_bot.sh`: Shell script for running the bot (used with cron)

## Usage

1. Run the bot manually:
   ```
   poetry run python bot.py
   ```

2. For automatic daily execution at 23:00, add to crontab:
   ```
   00 23 * * * /path/to/AmitSegalAISummarizer/run_bot.sh
   ```

## Configuration

To configure the source and destination channels, update the following constants in `util.py`:

- `SRC_CHANNEL_ID`: ID of Amit Segal's Telegram channel
- `DST_CHANNEL_ID`: ID of the destination channel for summaries

## Summary Format

The bot generates summaries in the following structure:

```
**עדכונים ביטחוניים:**
  • [Key point 1]
  • [Key point 2]
  ...

**עדכונים פוליטיים:**
  • [Key point 1]
  • [Key point 2]
  ...

**הציטוט היומי:**
  • `"[Significant quote from Amit Segal]"`
```

Sections are omitted if there are no relevant updates for that category.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Disclaimer

This bot uses AI to generate summaries. The summaries may contain inaccuracies. Always refer to the original messages in Amit Segal's channel for the most accurate information.
