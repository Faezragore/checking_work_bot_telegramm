import os
import requests
from dotenv import load_dotenv
import time
import telegram
import urllib.parse as urllib
import logging
from logging.handlers import RotatingFileHandler
from logging import StreamHandler


def main():
    devman_token = os.environ["DEVMAN_TOKEN"]
    headers = {
        'Authorization': 'Token %s' % (devman_token)
    }
    payload = {"timestamp":""}
    url = 'https://dvmn.org/api/long_polling/'
    while True:
        try:
            logger.info("Бот запущен")
            response = requests.get(url, headers=headers, verify=True, params=payload, timeout=100)
            response.raise_for_status()
            response_from_server = response.json()
            
        except requests.exceptions.HTTPError as e:
            logger.exception("ошибка exceptions.HTTPError")
            continue
        except requests.ReadTimeout as e:
            logger.exception("ошибка ReadTimeout ")
            continue
        except requests.ConnectionError as e:
            logger.exception("ошибка ConnectionError ")
            continue
        
        if "timeout" in response_from_server["status"]:
            payload["timestamp"] = response_from_server["timestamp_to_request"]
        else:
            new_response_from_server = response_from_server["new_attempts"][0]
            send_a_message_to_telegram_bot("У вас проверили работу:урок %s. Отправляем уведомления о проверке работ" % (new_response_from_server["lesson_title"]))
            payload["timestamp"] = new_response_from_server["timestamp"]
            continue

def send_a_message_to_telegram_bot(message):
    bot.send_message(chat_id=chat_id, text=message)
            
            
if __name__ == '__main__':
    load_dotenv()
    telegram_token_bot = os.environ["TELEGRAM_TOKEN_BOT"]
    telegram_token_bot_logger = os.environ["TELEGRAM_TOKEN_BOT_LOGGER"]
    bot = telegram.Bot(token=telegram_token_bot)
    bot_logger = telegram.Bot(token=telegram_token_bot_logger)
    chat_id = os.environ["CHAT_ID"]
    
    class MyLogsHandler(logging.Handler):

        def emit(self, record):
            log_entry = self.format(record)
            bot_logger.send_message(chat_id=chat_id, text=log_entry)

    
    formatter = logging.Formatter("%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s")
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.addHandler(MyLogsHandler())

    logger.info("Я новый логер!")
    main()
