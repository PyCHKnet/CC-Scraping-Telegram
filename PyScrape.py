import os
import re
import asyncio
from dotenv import load_dotenv
from telethon import TelegramClient, events

load_dotenv()

if os.path.exists('.env'):
    update = input("The .env file already exists, Do you want to update your API credentials? (y/n) ")
    if update.lower() == 'y':
        api_id = input("Enter your API ID: ")
        api_hash = input("Enter your API hash: ")
        group_id = input("Enter the group ID to scrape: ")
        session_name = input("Enter a name for your session: ")
        with open('.env', 'w') as f:
            f.write(f"API_ID={api_id}\n")
            f.write(f"API_HASH={api_hash}\n")
            f.write(f"GROUP_ID={group_id}\n")
            f.write(f"SESSION_NAME={session_name}\n")
    else:
        api_id = int(os.getenv('API_ID'))
        api_hash = os.getenv('API_HASH')
        group_id = int(os.getenv('GROUP_ID'))
        session_name = os.getenv('SESSION_NAME')
else:
    api_id = input("Enter your API ID: ")
    api_hash = input("Enter your API hash: ")
    group_id = input("Enter the group ID to scrape: ")
    session_name = input("Enter a name for your session: ")
    with open('.env', 'w') as f:
        f.write(f"API_ID={api_id}\n")
        f.write(f"API_HASH={api_hash}\n")
        f.write(f"GROUP_ID={group_id}\n")
        f.write(f"SESSION_NAME={session_name}\n")

client = TelegramClient(session_name, api_id, api_hash)

async def extract_card_info(message):
    text = message.message
    match = re.search(r'\b\d{15,16}\b', text)
    if match:
        card_number = match.group().replace(' ', '')
        month_match = re.search(r'(\b0?[1-9]\b|\b1[0-2]\b)[^\d]+(\d{2}|\d{4})', text)
        if month_match:
            month = month_match.group(1).zfill(2)
            year = month_match.group(2)
            if len(year) == 2:
                year = '20' + year
            cvv_match = re.search(r'\b\d{3}\b', text)
            if cvv_match:
                cvv = cvv_match.group()
                formatted_message = f"{card_number}|{month}|{year}|{cvv}"
                with open('card_info.txt', 'a') as f:
                    f.write(formatted_message + '\n')
                print(f'Card info extracted: {formatted_message}')

@client.on(events.NewMessage(chats=[group_id]))
async def extract_new_card_info(event):
    message = event.message
    await extract_card_info(message)

async def main():
    await client.start()
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())

