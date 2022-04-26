# импорт всех библиотек
import asyncio
import json
from telethon import TelegramClient, events, sync
from flask import Flask, request
from flask_ngrok import run_with_ngrok
import os
import threading
import requests  # для URL запроса
from bs4 import BeautifulSoup  # для работы с HTML
from flask import Flask
from pyngrok import ngrok, conf
import sqlite3
from data import db_session
from data.logs import Log

# импорт всех библиотек

os.environ["FLASK_ENV"] = "development"

# turn on the Flask server
app = Flask(__name__)
port = 5000

conf.get_default().auth_token = "1TAQMab2CGNEfLxOf5wPDf4UPCn_xQdDqeHaPDEEt96k9tee"
# Open a ngrok tunnel to the HTTP server
public_url = ngrok.connect(port).public_url
print(" * ngrok tunnel \"{}\" -> \"http://127.0.0.1:{}\"".format(public_url, port))
# turn on the Flask server

# Update any base URLs to use the public ngrok URL
app.config["BASE_URL"] = public_url


@app.route('/sample_page')
def return_sample_page():
    return f"""<!doctype html>
                <html lang="en">
                  <head>
                    <meta charset="utf-8">
                    <link rel="stylesheet" type="text/css" />
                    <title>Это бот яндекс алисы!</title>
                  </head>
                  <body>
                    <h1>Вы сюда не должны попадать.</h1>
                  </body>
                </html>"""


@app.route('/', methods=['POST', 'GET'])
def main():
    '''
    Эта функция реализует товет для сервера, который проверяет активность моей программы
    '''
    return 0


@app.route('/get-news', methods=['POST'])
def handler():
    '''
    Основная функция, в которой происходит распарсивание запроса пользователя
    '''
    event = request.get_json()
    log = Log()
    # check for the critical errors
    try:
        # print(event)
        """
        Entry-point for Serverless Function.
        :param event: request payload.
        :param context: information about current execution context.
        :return: response to be serialized as JSON.
        """
        text = 'Привет! Ты запустил навык. Я могу рассказать последнюю новость (Например: Покажи новость часа), ' \
               'через меня ты можешь узнать актуальный курс валют и криптовалют (например: курс криптовалюты биткоина), ' \
               'также я иогу включить мелодию для продуктивной работы.'
        if 'request' in event and \
                'original_utterance' in event['request'] \
                and len(event['request']['original_utterance']) > 0:
            message = event['request']['original_utterance']
            if "новост" in message.lower():
                return {
                    'version': event['version'],
                    'session': event['session'],
                    'response': {
                        # Respond with the original request or welcome the user if this is the beginning of the dialog and the request has not yet been made.
                        'text': text,
                        # Don't finish the session after this response.
                        'end_session': 'false',
                        "card": {
                            "type": "BigImage",
                            "image_id": "997614/22f003abcd201585777f",
                            "title": "Новость дня!",
                            "description": asyncio.run(telegramm_news()),
                            "button": {
                                "text": "Из канала Nedomainer",
                                "url": "https://t.me/nedomainer",
                                "payload": {}
                            }
                        }
                    }
                }
            elif "курс" in message.lower():
                if "акц" in message.lower():
                    temp = get_price(message.lower().split()[-1])
                    if temp == "Не найдено":
                        temp_reload = get_price(message.lower().split()[-1][:-1])
                        if temp_reload == "Не найдено":
                            text = "Извините по вашему запросу не найдено ни одного актива"
                        else:
                            text = "Актуальная цена: " + temp_reload
                    else:
                        text = "Актуальная цена: " + temp
                elif "валют" in message.lower():
                    if "крипт" in message.lower():
                        if not price_crypto(message.split()[-1]):
                            if not price_crypto(message.split()[-1][:-1]):
                                text = "Я вас не понимаю, переформулируйте запрос"
                            else:
                                text = "Актуальная цена: " + str(price_crypto(message.split()[-1][:-1]))
                        else:
                            text = "Актуальная цена: " + str(price_crypto(message.split()[-1]))
                    elif "доллар" in message.lower():
                        text = "Актуальная цена: " + str(convert_price(1))
                    elif "евро" in message.lower():
                        text = "Актуальная цена: " + str(convert_price_eur(1))
                    else:
                        text = "Я вас не понимаю, переформулируйте запрос"
            elif "мелод" in message.lower():
                return {
                    "tts": "<speaker audio=\"alice-sounds-game-win-1.opus\"> Вот расслабляющая мелодия!",
                    'version': event['version'],
                    'session': event['session'],
                    'response': {
                        # Respond with the original request or welcome the user if this is the beginning of the dialog and the request has not yet been made.
                        'text': "У вас получилось!",
                        'tts': '<speaker audio="dialogs-upload/1edebb40-2634-418e-991a-ff7e6a7f45b0/3ddd944b-2eb6-4e11-9181-9b8e1e6d4560.opus>"  Вот расслабляющая мелодия!',
                        # Don't finish the session after this response.
                        'end_session': 'false'

                    }
                }
            else:
                text = "Я вас не понимаю, переформулируйте запрос"
        # check for the critical errors
        log.status = "OK"
        db_sess = db_session.create_session()
        db_sess.add(log)
        db_sess.commit()
        # Response to the Yandex Alisa
        return {
            'version': event['version'],
            'session': event['session'],
            'tts': '<speaker audio="dialogs-upload/1edebb40-2634-418e-991a-ff7e6a7f45b0/3ddd944b-2eb6-4e11-9181-9b8e1e6d4560.opus"> У вас получилось!',
            'response': {
                # Respond with the original request or welcome the user if this is the beginning of the dialog and the request has not yet been made.
                'text': text,
                'tts': '<speaker audio="dialogs-upload/1edebb40-2634-418e-991a-ff7e6a7f45b0/3ddd944b-2eb6-4e11-9181-9b8e1e6d4560.opus>" У вас получилось!',
                # Don't finish the session after this response.
                'end_session': 'false'
            }
        }

    except:
        log.status = "Error"
        db_sess = db_session.create_session()
        db_sess.add(log)
        db_sess.commit()


def convert_price(value):
    '''
        Основная функция, в которой происходит конверт валют
    '''
    url = "https://free.currconv.com/api/v7/convert?q=USD_RUB&compact=ultra&apiKey=193dd415a8aea4ad6a8d"
    j = requests.get(url)
    data = json.loads(j.text)
    price = data['USD_RUB']
    return price * value


def convert_price_eur(value):
    '''
        функция, в которой происходит конверт валют
    '''
    url = "https://free.currconv.com/api/v7/convert?q=EUR_RUB&compact=ultra&apiKey=193dd415a8aea4ad6a8d"
    j = requests.get(url)
    data = json.loads(j.text)
    price = data['EUR_RUB']
    return price * value


def price_crypto(name_crypto):
    '''
            Основная функция, в которой происходит запрос на сервер
            для того, чтобы узнать текущий курс криптовалюты
        '''
    try:
        symbols = get_crypto_symbols(name_crypto)
        url = "https://api.bittrex.com/api/v1.1/public/getticker?market=USD-" + symbols
        prev_price = 0
        while True:
            j = requests.get(url)
            data = json.loads(j.text)
            price = data['result']['Ask']
            if price != prev_price:
                prev_price = price
                return toFixed(convert_price(price), 2)
    except:
        return False


async def telegramm_news():
    '''
                Основная функция, в которой происходит запрос на сервер
                для того, чтобы узнать текущую последнюю новость
            '''
    api_id = 14907003
    api_hash = 'b287149e82286c70b45565db8d37f67f'
    # api_id = 143790700563
    # api_hash = 'b287149e8228s6c70b455s65db8d3d7f67f'
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    client = TelegramClient('session_name', api_id, api_hash)
    await client.connect()
    channel_username = 'nedomainer'  # your channel
    otvet = ""
    i = 1
    for message in await client.get_messages(channel_username, limit=1):
        otvet = str(message.message)
        if not message.media == False:
            # NOT WORKING
            # await client.download_media(message, "save_path")
            # client.download_media(message)
            # NOT WORKING
            print(message)
            data = message.date
            file_name = "photo_" + str(data.year) + "-" + str(data.month).zfill(2) + "-" + str(data.day).zfill(2) + \
                        "_" + str(data.hour).zfill(2) + "-" + str(data.minute).zfill(2) + "-" + str(data.second).zfill(
                2) + ".jpg"
            if not os.path.exists("/save_path/" + file_name):
                name = await message.download_media(file="save_path")
        # post_image("save_path/photo_2022-04-26_05-59-04.jpg")
        print(message)
    return otvet


def get_price(company_name):
    # ссылка на тикер (Я использовал сайт google finance)
    '''
            Основная функция, в которой происходит запрос на сервер
            для того, чтобы узнать текущий курс акции компании
        '''
    try:
        url = "https://invest.yandex.ru/catalog/search/?text=" + str(company_name)
        headers = {
            'user agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/91.0.4472.135 Safari/537.36"}
        html = requests.get(url, headers)
        soup = BeautifulSoup(html.content, 'html.parser')
        convert = soup.findAll('div', {'class': 'JGT__mSaFfXxcOb2oGto'})
        return convert[0].text[:]
    except:
        return "Не найдено"


def get_krypti_currency():
    with open("Investing.html", "r", encoding='utf-8') as f:
        soup = BeautifulSoup(f, "html.parser")
    currency_names = soup.findAll('td', {'class': 'js-currency-name'})
    currency_symbols = soup.findAll('td', {'class': 'js-currency-symbol'})
    dict_of_crypto = {}
    for i in range(len(currency_names)):
        dict_of_crypto[currency_names[i].get_text()] = currency_symbols[i].get_text()
    print(dict_of_crypto)
    full_database(dict_of_crypto)
    return 0

    # print("Цена акции Газпром: ", price)


def create_table_currency():
    '''
                Основная функция, в которой происходит
                создание базы данных названиями и символами криптовалют
            '''
    # Connecting to sqlite
    # get the count of tables with the name
    conn = sqlite3.connect('alisa.db')
    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()
    cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='crypto' ''')

    # if the count is 1, then table exists
    if cursor.fetchone()[0] == 1:
        conn.close()
        return 0
    else:
        # Creating table as per requirement
        sql = '''CREATE TABLE IF NOT EXISTS crypto(
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           name VARCHAR(20) NOT NULL,
           symbol VARCHAR(20) NOT NULL
        )'''
        cursor.execute(sql)
        # Commit your changes in the database
        conn.commit()
        # Closing the connection
        conn.close()
        return 1


'''
Основная функция, в которой происходит
возврат запроса на воспроизведение аудио
'''


def response_media_music():
    return {
        "response": {
            "text": "вот хорошая песня",
            "tts": "вот хорошая песня",
            "end_session": False,
            "should_listen": False,
            "directives": {
                "audio_player": {
                    "action": "Play",
                    "item": {
                        "stream": {
                            "url": "https://example.com/stream-audio-url",
                            "offset_ms": 0,
                            "token": "token"
                        },
                        "metadata": {
                            "title": "Песня",
                            "sub_title": "Артист",
                            "art": {
                                "url": "https://example.com/art.png"
                            },
                            "background_image": {
                                "url": "https://example.com/background-image.png"
                            }
                        }
                    }
                }
            }
        },
        "version": "1.0"
    }


'''
Основная функция, в которой происходит
возврат запроса на воспроизведение аудио
'''


def full_database(dictionary):
    '''
                    Основная функция, в которой происходит
                    заполнение базы данных названиями и символами криптовалют
                '''
    # Connecting to sqlite
    conn = sqlite3.connect('alisa.db')
    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()
    # Creating table as per requirement
    for i, j in dictionary.items():
        sql = '''INSERT INTO crypto
        (name, symbol) VALUES (?,?)
            '''
        cursor.execute(sql, (i.lower(), j))
        # Commit your changes in the database
        conn.commit()
    # Closing the connection
    conn.close()


def get_crypto_symbols(human_word):
    '''
                        Основная функция, в которой происходит
                        завпрос в базу данных с названиями и символами криптовалют
                    '''
    # Connecting to sqlite
    conn = sqlite3.connect('alisa.db')
    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()
    # Creating table as per requirement
    result = cursor.execute("""SELECT * FROM crypto
                    WHERE name = ?""", [human_word]).fetchall()
    # Closing the connection
    conn.close()
    return result[0][2]


def toFixed(numObj, digits=0):
    return f"{numObj:.{digits}f}"


def post_image(img_file):
    """ post image and return the response """

    # img = open(img_file, 'rb').read()
    data = {"file": open(img_file, 'rb')}
    # print(img)
    headers = {"Authorization": "OAuth AQAAAAASbJX-AAT7o4BVujPtpkhto4JwFfY55jI",
               "Content-Type": "multipart/form-data;boundary=1111", "Content-Length": str(os.path.getsize(img_file))}
    response = requests.post("https://dialogs.yandex.net/api/v1/skills/1edebb40-2634-418e-991a-ff7e6a7f45b0/images",
                             files=data, headers=headers)
    print(response.json())
    return response


if __name__ == '__main__':
    #     app.run()
    db_session.global_init("db/logs.db")
    if create_table_currency():
        get_krypti_currency()
    threading.Thread(target=app.run, kwargs={"use_reloader": False}).start()
