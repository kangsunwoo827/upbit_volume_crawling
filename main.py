from crawler import Crawler
import json
import telegram
import asyncio
import datetime
current_date = datetime.datetime.now()
days_of_week = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

# 날짜 출력
formatted_date = current_date.strftime('%y년 %m월 %d일(') + days_of_week[current_date.weekday()] + ')'
krw_volume=Crawler().getVolumes()

volume_text = '{:.3f}조'.format(krw_volume/(10**12))
send_text = f'{formatted_date} 업비트 24시간 누적 거래량: {volume_text} KRW'


api_key = json.load(open('secret.json'))['BotKey']

bot = telegram.Bot(token = api_key)

chat_id = json.load(open('secret.json'))['ChatID']


asyncio.run(bot.send_message(chat_id = chat_id, text=send_text))