import os
import requests
from dotenv import load_dotenv
import time
import telegram
import urllib.parse as urllib
import logging
from logging.handlers import RotatingFileHandler


logging.basicConfig(format = '%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level = logging.INFO)


def main():
    devman_token = os.getenv("DEVMAN_TOKEN")
    headers = {
        'Authorization': 'Token %s' % (devman_token)
    }
    payload = {"timestamp":""}
    url = 'https://dvmn.org/api/long_polling/'
    while True:
        try:
            logging.info("Бот запущен")
            response = requests.get(url, headers=headers, verify=True, params=payload, timeout=100)
            response.raise_for_status()
            response_from_server = response.json()
        except requests.exceptions.HTTPError:
            logging.exception()
            continue
        except requests.ReadTimeout:
            continue
        except requests.ConnectionError:
            continue
        
        if "timeout" in response_from_server["status"]:
            payload["timestamp"] = response_from_server["timestamp_to_request"]
        else:
            new_response_from_server = response_from_server["new_attempts"][0]
            send_a_message_to_telegram_bot("У вас проверили работу:урок %s. Отправляем уведомления о проверке работ" % (new_response_from_server["lesson_title"]))
            payload["timestamp"] = new_response_from_server["timestamp"]
            continue


def send_a_message_to_telegram_bot(message):
    telegram_token = os.getenv("TELEGRAM_TOKEN")
    bot = telegram.Bot(token=telegram_token)
    chat_id = os.getenv("CHAT_ID")
    bot.send_message(chat_id=chat_id, text=message)


if __name__ == '__main__':
    load_dotenv()
    main()
