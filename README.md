# xkcd Telegram Bot
A telegram bot that notifies you whenever a new xkcd is released. You can also use it to send xkcd comics in group chats.

## Dependencies
* [python3](https://www.python.org)
* [python-requests](https://github.com/requests/requests/)
* [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)

## Usage
Simply clone the project, insert your Telegram API token in the indicated space inside `main.py` and run `main.py` using the Python 3 interpreter.

## Commands
The bot supports the following commands:
* **/subscribe** - It will notify you whenever a new xkcd comic is released.
* **/unsubscribe** - You'll stop being notified when new xkcd comics are released.
* **/xkcd [comic number]** - Sends you the xkcd comic you ask for. Send no comic number and it will send you the latest comic.
* **/random** - Sends you a random xkcd comic.

## Hosted Version
Don't want to host the bot yourself? There is a working bot hosted by me. You can reach it at [@xkcdnotifierbot](https://t.me/xkcdnotifierbot)!
