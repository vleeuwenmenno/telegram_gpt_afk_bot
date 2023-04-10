# ChatGPT Telegram Bot

This is a Telegram bot that uses OpenAI's API to generate responses to messages. The bot is designed to work in a one-to-one conversation but can also be used in group chats although it is not recommended.

The goal of this bot is to turn it on when you're busy so it can respond to your friends' messages for you. You can also use it to have a conversation with yourself but remember that there's a chat history limit so you might not be able to go back to previous messages too far and keep in mind the cost per 1000 tokens of using OpenAI's API.

Also note that this bot is not affiliated with OpenAI in any way. It is just a personal project I made for fun. If you want to use OpenAI's API, you should sign up for an account [here](https://openai.com/).

## Requirements

- Python 3.8 or higher
- A Telegram API ID and API Hash
- An OpenAI API key

## Getting Started

1. Clone this repository and navigate into it.
2. Install dependencies using `pip install -r requirements.txt`
3. Get your Telegram API Credentials from [my.telegram.org](https://my.telegram.org). See [this guide](https://core.telegram.org/api/obtaining_api_id) for instructions on how to get your API credentials.
4. Create an OpenAI API key. See [this guide](https://beta.openai.com/docs/quickstart) for instructions on how to get an API key.
5. Create a `.env` file in the root of the project directory with the following contents:

```
    TELEGRAM_API_ID=<your_telegram_api_id>
    TELEGRAM_API_HASH=<your_telegram_api_hash>
    TELEGRAM_SAVED_MESSAGES_CHAT_ID=<your_telegram_saved_messages_chat_id>
    OPENAI_API_KEY=<your_openai_api_key>
    CHAT_HISTORY_LIMIT=<your_chat_history_limit>
    REPLY_ON_GROUP_CHATS=<true_or_false>
```
6. Replace the placeholders in the `.env` file with your own values. Note that `TELEGRAM_SAVED_MESSAGES_CHAT_ID` is the chat ID of your Saved Messages chat.
7. Run `python main.py` to start the bot.

## Notes

- The bot will respond to any messages sent to it in a one-to-one conversation. It will not respond to messages in group chats unless `REPLY_ON_GROUP_CHATS` is set to `true` in the `.env` file.
- When the bot receives a message, it will generate a response using OpenAI's GPT-3.5-Turbo model. The response will be sent back to the user.
- If the user sends an emoji or an empty message, the bot will not generate a response.
- The bot will store a chat history for each user it interacts with. If the chat history reaches the `CHAT_HISTORY_LIMIT` (specified in the `.env` file), the bot will remove the oldest message in the history.
- Part of this README was written using the bot itself.