#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to send timed Telegram messages.
This Bot uses the Updater class to handle the bot and the JobQueue to send
timed messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Alarm Bot example, sends a message after a set time.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

import telegram
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters


import telebot  # Подключили библиотеку Телебот - для работы с Телеграм
from telebot import types  # Подключили дополнения
# import config  # Подключили библиотеку Config, с помощью чего можем хранить токен не в коде программы ;) а в файле
# config.py. Важно: этот файл должен лежать в той же директории, что и код!

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

bot = telebot.TeleBot("1880644245:AAFTj1CL2LKTtKhVaEcL-a0i0RkwoRrD9EU")  # Подключили токен


# @bot.message_handler(commands=['number'])  # Объявили ветку для работы по команде <strong>number</strong>
@bot.message_handler(commands=['start'])  # Объявили ветку для работы по команде <strong>number</strong>
def phone(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)  # Подключаем клавиатуру
    button_phone = types.KeyboardButton(text="Отправить телефон",
                                        request_contact=True)  # Указываем название кнопки, которая появится у
    # пользователя
    keyboard.add(button_phone)  # Добавляем эту кнопку
    #keyboard.selective = False
    bot.send_message(message.chat.id, 'Номер телефона',
                     reply_markup=keyboard)  # Дублируем сообщением о том, что пользователь сейчас отправит боту свой
    # номер телефона (на всякий случай, но это не обязательно)


# @bot.message_handler(commands=['number'])  # Объявили ветку для работы по команде <strong>number</strong>
'''
@bot.message_handler(commands=['location'])  # Объявили ветку для работы по команде <strong>number</strong>
def phone(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)  # Подключаем клавиатуру
    button_phone = types.KeyboardButton(text="Отправить геолокацию",
                                        request_location=True)  # Указываем название кнопки, которая появится у пользователя
    keyboard.add(button_phone)  # Добавляем эту кнопку
    bot.send_message(message.chat.id, 'Отправить геолокацию', reply_markup=keyboard)  # Дублируем сообщением о том, что 
    #пользователь сейчас отправит боту свой номер телефона (на всякий случай, но это не обязательно)
'''


@bot.message_handler(content_types=['contact'])  # Объявили ветку, в которой прописываем логику на тот случай,
# если пользователь решит прислать номер телефона :)
def contact(message):
    if message.contact is not None:  # Если присланный объект <strong>contact</strong> не равен нулю
        print(message.contact)  # Выводим у себя в панели контактные данные. А вообщем можно их, например, сохранить
        # или сделать что-то еще.
        # {'phone_number': '79774599118', 'first_name': 'Oulina', 'last_name': 'Art', 'user_id': 347179990,
        # 'vcard': None}


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)


def start(update: Update, context: CallbackContext) -> None:
    """Sends explanation on how to use the bot."""
    update.message.reply_text('Hi! Use /set <seconds> to set a timer')
    print(update.message)

    # https://stackoverflow.com/questions/34567920/in-python-telegram-bot-how-to-get-all-participants-of-the-group
    # {'new_chat_photo': [], 'chat':
    # {'last_name': 'Art', 'type': 'private', 'first_name': 'Oulina', 'username': 'Oulina', 'id': 347179990},
    # 'delete_chat_photo': False, 'text': '/start', 'message_id': 210,
    # 'entities': [{'type': 'bot_command', 'offset': 0, 'length': 6}], 'photo': [], 'group_chat_created': False,
    # 'caption_entities': [], 'date': 1646133867, 'channel_chat_created': False, 'new_chat_members': [],
    # 'supergroup_chat_created': False, 'from': {'is_bot': False, 'last_name': 'Art', 'username': 'Oulina',
    # 'language_code': 'en', 'first_name': 'Oulina', 'id': 347179990}}


def get_data(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)
    print(context._user_id_and_data)  # (347179990, {}) - (347179990, {}) - (503785483, {})
    contact = update.effective_message.contact
    # phone = contact.phone_number
    print(contact)


def alarm(context: CallbackContext) -> None:
    """Send the alarm message."""
    job = context.job
    context.bot.send_message(job.context, text='Beep!')


def remove_job_if_exists(name: str, context: CallbackContext) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


def set_timer(update: Update, context: CallbackContext) -> None:
    """Add a job to the queue."""
    chat_id = update.message.chat_id
    print(chat_id)
    try:
        # args[0] should contain the time for the timer in seconds
        due = int(context.args[0])
        if due < 0:
            update.message.reply_text('Sorry we can not go back to future!')
            return

        job_removed = remove_job_if_exists(str(chat_id), context)
        context.job_queue.run_once(alarm, due, context=chat_id, name=str(chat_id))

        text = 'Timer successfully set!'
        if job_removed:
            text += ' Old one was removed.'
        update.message.reply_text(text)

    except (IndexError, ValueError):
        update.message.reply_text('Usage: /set <seconds>')


def unset(update: Update, context: CallbackContext) -> None:
    """Remove the job if the user changed their mind."""
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = 'Timer successfully cancelled!' if job_removed else 'You have no active timer.'
    update.message.reply_text(text)


def main() -> None:
    """Run bot."""
    # updater = Updater("5235947184:AAE1erfSSltFnjQPxAt-GgL8DgHYa9vzaLk")
    updater = Updater("1880644245:AAFTj1CL2LKTtKhVaEcL-a0i0RkwoRrD9EU")

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", start))
    dispatcher.add_handler(CommandHandler("set", set_timer))
    dispatcher.add_handler(CommandHandler("unset", unset))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, get_data))

    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    # main()

    bot.infinity_polling()





