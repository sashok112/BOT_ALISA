# # dictionary = {
# #   "meta": {
# #     "locale": "ru-RU",
# #     "timezone": "UTC",
# #     "client_id": "ru.yandex.searchplugin/7.16 (none none; android 4.4.2)",
# #     "interfaces": {
# #       "screen": {},
# #       "payments": {},
# #       "account_linking": {}
# #     }
# #   },
# #   "session": {
# #     "message_id": 1,
# #     "session_id": "c728eb59-e414-4046-998e-e2fb46624196",
# #     "skill_id": "1edebb40-2634-418e-991a-ff7e6a7f45b0",
# #     "user": {
# #       "user_id": "7914E1F3B0F96EA71602FFC63B130ADC0657F846A524E842EC59965860D52041"
# #     },
# #     "application": {
# #       "application_id": "08BF5A9B394139257133B8F90A42CA108B3D5D4610F61E8391992ED52E261159"
# #     },
# #     "new": False,
# #     "user_id": "08BF5A9B394139257133B8F90A42CA108B3D5D4610F61E8391992ED52E261159"
# #   },
# #   "request": {
# #     "command": "новост",
# #     "original_utterance": "Новост",
# #     "nlu": {
# #       "tokens": [
# #         "новост"
# #       ],
# #       "entities": [],
# #       "intents": {}
# #     },
# #     "markup": {
# #       "dangerous_context": False
# #     },
# #     "type": "SimpleUtterance"
# #   },
# #   "version": "1.0"
# # }
# # print(handler(dictionary, ""))
# def handler(event, context):
#     """
#     Entry-point for Serverless Function.
#     :param event: request payload.
#     :param context: information about current execution context.
#     :return: response to be serialized as JSON.
#     """
#
#     text = 'Привет! Ты запустил навык.'
#     api_id = 14907003
#     api_hash = 'b287149e82286c70b45565db8d37f67f'
#
#     client = TelegramClient('session_name', api_id, api_hash)
#     client.start(phone="+79647162004")
#
#     if 'request' in event and \
#             'original_utterance' in event['request'] \
#             and len(event['request']['original_utterance']) > 0:
#         message = event['request']['original_utterance']
#         if "новост" in message.lower():
#             text = telegramm_news()
#     return {
#         'version': event['version'],
#         'session': event['session'],
#         'response': {
#             # Respond with the original request or welcome the user if this is the beginning of the dialog and the request has not yet been made.
#             'text': text,
#             # Don't finish the session after this response.
#             'end_session': 'false'
#         },
#     }
#
# import asyncio
# from telethon import TelegramClient
#
# api_id = 14907003
# api_hash = 'b287149e82286c70b45565db8d37f67f'
# bot_token = '5105632720:AAFmNrkAtI-QlH5lpIlpMvQEZK6TdZbWUxI'
#
#
# def main():
#     started = TelegramClient('anon', api_id, api_hash).start()
#     if not isinstance(started, TelegramClient):
#         raise ValueError(f"Unexpected client: {started}")
#     async with started as client:
#         pass
#
#
# asyncio.run(main())

# # from telethon import TelegramClient, events, sync
# # import asyncio
# #
# # api_id = 14907003
# # api_hash = 'b287149e82286c70b45565db8d37f67f'
# #
# #
# # client = TelegramClient('session_name', api_id, api_hash)
# # client.start(phone="+79647162004", password="Sasha0707")
# # channel_username = 'nedomainer' # your channel
# # for message in client.get_messages(channel_username, limit=10):
# #     print(message.message)
# #
# # def main():
# #     phone = "+79647162004"
# #     y = client.send_code_request(phone)
# #     print(y.phone_code_hash)
# #     # client.sign_in(phone=phone, password="Sasha0707", code=61975)
# #     # client = TelegramClient('anon', api_id, api_hash)
# #     # assert await client.connect()
# #     # if not client.is_user_authorized():
# #     #     await client.send_code_request(phone_number)
# #     #     me = await client.sign_in(phone_number, input('Enter code: '))
# #
# #
# # main()
# #
# #
# # #
# # # class TelegramClientFactory:
# # #     @staticmethod
# # #     async def login():
# # #         api_id = 14907003
# # #         api_hash = 'b287149e82286c70b45565db8d37f67f'
# # #         phone_number = '+79647162004'
# # #         user_name = 'Alex'
# # #         password = 'Sasha0707'
# # #
# # #         client = TelegramClient(user_name, api_id, api_hash)
# # #         await client.connect()
# # #
# # #         if not await client.is_user_authorized():
# # #             await client.send_code_request(phone_number)
# # #             try:
# # #                 await client.sign_in(phone_number, input('Enter code: '))
# # #             except Exception:
# # #                 await client.sign_in(password=password)
# # #
# # #         return client
# # #
# # #     @staticmethod
# # #     def get_instance() -> object:
# # #         loop = asyncio.new_event_loop()
# # #         asyncio.set_event_loop(loop)
# # #         task = loop.create_task(TelegramClientFactory.login())
# # #         client = loop.run_until_complete(task)
# # #         return client
# # #
# # # factory = TelegramClientFactory()
# # # factory.get_instance()
# # # import telebot  # Подключили библиотеку Телебот - для работы с Телеграм
# # # from telebot import types  # Подключили дополнения
# # #
# # # bot = telebot.TeleBot("5105632720:AAFmNrkAtI-QlH5lpIlpMvQEZK6TdZbWUxI")
# # #
# # #
# # # @bot.message_handler(func=lambda message: True)
# # # def echo_all(message):
# # #     bot.reply_to(message, message.text)
# import asyncio
#
# import requests
# from telethon import TelegramClient, events, sync
# import threading
#
#
# async def telegramm_news():
#     api_id = 14907003
#     api_hash = 'b287149e82286c70b45565db8d37f67f'
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     client = TelegramClient('session_name', api_id, api_hash)
#     await client.start()
#     channel_username = 'nedomainer'  # your channel
#     messages = await client.get_messages(channel_username, limit=1)
#
#     if not messages[0].media == False:
#         print(messages[0].media)
#         name = await client.download_media(messages[0], "save_path")
#         print(name)
#         post_image(name)
#
#     # for message in await client.get_messages(channel_username, limit=1):
#     #     otvet = str(message.message)
#     #     if not message.media == False:
#     #         # upload.getFile
#     #         await client.download_media(message, "/save_path")
#     #
#     #         # client.download_media(messages[0])
#     #         # await message.download_media(file="/save_path")
#     #     print(message)
#
#


#
# if __name__ == '__main__':
#     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
#     asyncio.run(telegramm_news())
# import requests  # для URL запроса
# from bs4 import BeautifulSoup  # для работы с HTML
#
#
# def get_price(company_name):
#     # ссылка на тикер (Я использовал сайт google finance)
#     try:
#         url = "https://invest.yandex.ru/catalog/search/?text=" + str(company_name)
#         headers = {
#             'user agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) "
#                           "AppleWebKit/537.36 (KHTML, like Gecko) "
#                           "Chrome/91.0.4472.135 Safari/537.36"}
#         html = requests.get(url, headers)
#         soup = BeautifulSoup(html.content, 'html.parser')
#         convert = soup.findAll('div', {'class': 'JGT__mSaFfXxcOb2oGto'})
#         return convert[0].text[:]
#     except:
#         return "Не найдено"
#     # print("Цена акции Газпром: ", price)
#
#
# print(get_price("аэрофлот"))
# import requests
# import json
# import time
#
# url = "https://api.bittrex.com/api/v1.1/public/getticker?market=USD-ETH" #Так же можно получить цену другой криптовалюты вместо BTC - ETH - XRP - DOGE и.т.д
# INTERVAL = 1
# prev_price = 0
# while True:
#     j = requests.get(url)
#     data = json.loads(j.text)
#     price = data['result']['Ask']
#     if price!=prev_price:
#         prev_price = price
#         print('BTC PRICE: ' + str(price) + ' $')
#     time.sleep(INTERVAL)
#
# from bs4 import BeautifulSoup  # для работы с HTML
# from html.parser import HTMLParser
# import sqlite3
#
#
# def get_krypti_currency():
#     with open("Investing.html", "r", encoding='utf-8') as f:
#         parser = HTMLParser()
#         soup = BeautifulSoup(f, "html.parser")
#     currency_names = soup.findAll('td', {'class': 'js-currency-name'})
#     currency_symbols = soup.findAll('td', {'class': 'js-currency-symbol'})
#     dict_of_crypto = {}
#     for i in range(len(currency_names)):
#         dict_of_crypto[currency_names[i].get_text()] = currency_symbols[i].get_text()
#     print(dict_of_crypto)
#     create_table_currency()
#     full_database(dict_of_crypto)
#     return 0
#
#     # print("Цена акции Газпром: ", price)
#
# def create_table_currency():
#     # Connecting to sqlite
#     conn = sqlite3.connect('alisa.db')
#     # Creating a cursor object using the cursor() method
#     cursor = conn.cursor()
#     # Creating table as per requirement
#     sql = '''CREATE TABLE IF NOT EXISTS crypto(
#        id INTEGER PRIMARY KEY AUTOINCREMENT,
#        name VARCHAR(20) NOT NULL,
#        symbol VARCHAR(20) NOT NULL
#     )'''
#     cursor.execute(sql)
#     # Commit your changes in the database
#     conn.commit()
#     # Closing the connection
#     conn.close()
#
# def full_database(dictionary):
#     # Connecting to sqlite
#     conn = sqlite3.connect('alisa.db')
#     # Creating a cursor object using the cursor() method
#     cursor = conn.cursor()
#     # Creating table as per requirement
#     for i, j in dictionary.items():
#         sql = '''INSERT INTO crypto
#         (name, symbol) VALUES (?,?)
#             '''
#         cursor.execute(sql, (i, j))
#         # Commit your changes in the database
#         conn.commit()
#     # Closing the connection
#     conn.close()
#
#
# print(get_krypti_currency())
import json
import os.path
from urllib.parse import urljoin

from bs4 import BeautifulSoup
import requests


#
#
# def get_products(search: str) -> list:
#     headers = {
#         'X-Requested-With': 'XMLHttpRequest',
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'
#     }
#     url = f'https://www.dns-shop.ru/search/?q={search}&p=1&order=popular&stock=all'
#     session = requests.session()
#     session.headers.update(headers)
#
#     rs = session.get(url)
#     print(rs.text)
#     data = json.loads(rs.text)
#
#     root = BeautifulSoup(data['html'], 'html.parser')
#
#     items = []
#
#     for a in root.select('.product-info__title-link > a'):
#         items.append(
#             (a.get_text(strip=True), urljoin(rs.url, a['href']))
#         )
#
#     return items
#
# if __name__ == '__main__':
#     name = 'Видеокарты'
#     items = get_products(name)
#
#     print(f'Search {name!r}...')
#     print(f'  Result ({len(items)}):')
#     for title, url in items:
#         print(f'    {title!r}: {url}')
#     print()



