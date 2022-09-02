# -*- coding: utf-8 -*-
import os
import requests
from dotenv import load_dotenv
import time
import telegram
import urllib.parse as urllib
import logging
from logging.handlers import RotatingFileHandler
from logging import StreamHandler
import asyncio


logger = logging.getLogger('Бот логер')


class LogsHandler(logging.Handler):
    def __init__(self, tg_bot, tg_chat_id):
        super().__init__()
        self.tg_bot = tg_bot
        self.tg_chat_id = tg_chat_id

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(text=log_entry, chat_id=self.tg_chat_id)


def main():
    load_dotenv()
    telegram_token_bot = os.environ["TELEGRAM_TOKEN_BOT"]
    bot = telegram.Bot(token=telegram_token_bot)
    chat_id = os.environ["CHAT_ID"]
    devman_token = os.environ["DEVMAN_TOKEN"]

    formatter = logging.Formatter("%(filename)s[LINE:\
                %(lineno)d]# %(levelname)-8s [%(asctime)s]\
                %(message)s")
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.addHandler(LogsHandler(bot, chat_id))
    logger.info("Я новый логер!")
    logger.info("Бот запущен")

    headers = {
        'Authorization': 'Token %s' % (devman_token)
    }
    payload = {"timestamp": ""}
    url = 'https://dvmn.org/api/long_polling/'

    while True:
        try:
            response = requests.get(
                url, headers=headers,
                verify=True, params=payload, timeout=100
            )
            response.raise_for_status()
            response_api_devman = response.json()

            if "timeout" in response_api_devman["status"]:
                payload["timestamp"] = \
                    response_api_devman["timestamp_to_request"]
            else:
                new_response_api_devman = \
                    response_api_devman["new_attempts"][0]
                message = "У вас проверили работу:урок %s.\
                           Отправляем уведомления о проверке работ" \
                          % (new_response_api_devman["lesson_title"])
                bot.send_message(chat_id=chat_id, text=message)
                payload["timestamp"] = new_response_api_devman["timestamp"]
                continue

        except requests.exceptions.HTTPError as error:
            logger.exception("ошибка exceptions.HTTPError")
            continue
        except requests.ReadTimeout as error:
            logger.exception("ошибка ReadTimeout ")
            continue
        except requests.ConnectionError as error:
            logger.exception("ошибка ConnectionError ")
            continue
        except Exception as error:
            logger.exception("Бот упал с ошибкой: {error}")


if __name__ == '__main__':
    main()
