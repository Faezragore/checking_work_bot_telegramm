## Бот проверки учебных работ DEVMAN

#### Описание
Данная программа делает запрос на сервер Devman, и с помощью Telegram возвращает статус проверки учебных упражнений.

#### Как установить
Склонировать проект.

Python3 должен быть уже установлен. Затем используйте pip (или pip3, есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```
### Переменные
Cоздайте файл __.env__ и подставьте данные в файл.

TELEGRAM_TOKEN_BOT = 'токен бота от имени которого будут идти оповещения'

DEVMAN_TOKEN = 'токен доступа для API серверов Devman'

CHAT_ID = 'ID чата, в который будут идти сообщения бота'

Пример файла __.env__
```
DEVMAN_TOKEN=
TELEGRAM_TOKEN_BOT=
CHAT_ID=
```
### Запуск
* Откройте командную строку.
* Зайдите в репозиторий.
* Запустите скрипт командой  ```python setup.py ```
* В Телеграмм канал,который вы указали в переменной ```CHAT_ID``` будут приходить сообщения.

### Особенность
Данный скрипт работает пока запущен в командной строке.

Чтобы он работал постоянно,требуется размещение на отдельном сервере.

Для учебных целей можно разместить его в сервис [Heroku](https://www.heroku.com/).

#### Цель проекта
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org)
