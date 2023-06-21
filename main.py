from crawler import Crawler
import json
import telegram
import asyncio

krw_volume=Crawler().getVolumes()
volume_text = format(krw_volume,',')
send_text = f'24 hour accumulated trade value of Upbit is {volume_text} KRW'



api_key = json.load(open('secret.json'))['BotKey']

bot = telegram.Bot(token = api_key)

chat_id = json.load(open('secret.json'))['ChatID']


asyncio.run(bot.send_message(chat_id = chat_id, text=send_text))