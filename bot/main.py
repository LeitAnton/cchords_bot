import os
import sqlite3
from database import Database
from bot import TelegramBOT


if __name__ == '__main__':
    try:
        connection = sqlite3.connect("../database.sqlite")
        cursor = connection.cursor()

        database = Database(connection, cursor)
        database.create_tables()
        BOT_TOKEN = os.environ.get('BOT_TOKEN')
        bot = TelegramBOT(BOT_TOKEN)
    finally:
        connection.close()
