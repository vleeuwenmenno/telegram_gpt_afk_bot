import asyncio
import os
import openai
from telethon import TelegramClient, events

api_id = os.environ.get('TELEGRAM_API_ID')
api_hash = os.environ.get('TELEGRAM_API_HASH')

# Define key value pair list of chat ids and openai chat objects
chat_ids = []

# Define function that takes string as input and returns false or true based on if the string is an emoji
def is_emoji(s):
    return s in [chr(i) for i in range(0x1F600, 0x1F650)]

async def main():
    # Get the saved messages chat id as integer
    savedMessagesChatId = int(os.environ.get('TELEGRAM_SAVED_MESSAGES_CHAT_ID'))
    chatHistoryLimit = int(os.environ.get('CHAT_HISTORY_LIMIT'))
    replyOnGroupChats = os.environ.get('REPLY_ON_GROUP_CHATS').capitalize == "TRUE"

    # Prepare OpenAI
    openai.api_key = os.environ.get('OPENAI_API_KEY')
    
    # Prepare Telegram
    async with TelegramClient('session_name', api_id, api_hash) as client:
        me = await client.get_me()
        print("Logged in as", me.username)

        @client.on(events.NewMessage())
        async def handler(event: events.NewMessage.Event):

            user = await event.get_sender()

            # If message is from a group chat, check if we should reply
            if event.is_group and not replyOnGroupChats:
                return
            
            # Let's check if the message is empty, if so we'll ignore it
            if event.message.message == "":
                return
            
            # Let's check if the message starts with ChatGPT, if so we'll ignore it
            if event.message.message.startswith("ChatGPT:"):
                return
            
            # Let's check if the message is from myself but continue if the chat id is the saved messages chat
            if user.id == me.id and event.chat_id != savedMessagesChatId:
                return
            
            if (is_emoji(event.message.message)):
                return
        
            print(f"[{event.chat_id}] [ MSG ] {user.first_name} {user.last_name}: {event.message.message}")
            response = await event.reply(f"`ChatGPT is thinking ... ({me.first_name} {me.last_name} is away so I'm filling in)`") 

            # Get the chat object from the list
            chatHistory = []

            # Check if the chat id is already in the list
            if not any(chat_id["id"] == user.id for chat_id in chat_ids):
                chatHistory=[ 
                    {
                        "role": "system",
                        "content": f"You are speaking for {me.first_name} {me.last_name} and you are filling in for me as an AI."
                    },
                    {
                        "role": "system", 
                        "content": f"A message came in from {user.first_name} {user.last_name}, make sure to tell him/her that you're filling in for me as an AI and that I'm busy at the moment"
                    },
                    {
                        "role": "system", 
                        "content": f"Please reply to the message to the best of your abilities but keep it concise and also make sure to reply in the language based on the given message, make sure you're 100% sure it's that otherwise just fall back to English."
                    }
                ]
            else:
                chatHistory = next(chat_id["chat"] for chat_id in chat_ids if chat_id["id"] == user.id)
            
            print(f"[{event.chat_id}] [ GPT ] [ {len(chatHistory)}/{chatHistoryLimit} ] Generating response for {user.first_name} {user.last_name}")

            # Add the new message to the chat object
            chatHistory.append({ "role": "user", "content": event.message.message })

            # Let's ask OpenAI for our next response, use the original chat object
            chat = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=chatHistory
            )
            content = chat["choices"][0]["message"]["content"]
            chatHistory.append({ "role": "assistant", "content": content })

            # Send the response to the user
            await client.send_message(event.chat_id, f"ChatGPT: ```{content}```")
            print(f"[{event.chat_id}] [ GPT ] [ {len(chatHistory)}/{chatHistoryLimit} ] Replied to {user.first_name} {user.last_name} with a OpenAI response.")

            # If the chat history is >= CHAT_HISTORY_LIMIT, messages remove the oldest message
            if len(chatHistory) >= chatHistoryLimit:
                print(f"[{event.chat_id}] [ GPT ] [ {len(chatHistory)}/{chatHistoryLimit} ] Chat history is full, removing oldest message.")

            # Remove chat object from the list if it's already in the list
            if any(chat_id["id"] == user.id for chat_id in chat_ids):
                chat_ids.remove(next(chat_id for chat_id in chat_ids if chat_id["id"] == user.id))

            # Add the updated chat object to the list
            chat_ids.append({ "id": event.chat_id, "chat": chatHistory })
                         
            await client.delete_messages(event.chat_id, response.id)

        await client.run_until_disconnected()

asyncio.run(main())