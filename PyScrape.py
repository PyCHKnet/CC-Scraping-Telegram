import re
import asyncio
from telethon import TelegramClient, events

api_id = 27197543 # enter your telegram api_id 
api_hash = '8f530b22c5b15b480839087f26bdb4d3' # enter your telegram_id hash
session_name = 'my_session' #anything here you would like

client = TelegramClient(session_name, api_id, api_hash)

group_id = 123456 #group id where you want to scrape ccs from

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

asyncio.run(main())

