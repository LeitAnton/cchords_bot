import os
import sqlite3
from database import Database, create_tables
from bot import TelegramBOT


if __name__ == '__main__':
    connection = None
    try:
        connection = sqlite3.connect("../database.sqlite", check_same_thread=False)
        cursor = connection.cursor()

        create_tables(connection, cursor)
        database = Database(connection, cursor)

        BOT_TOKEN = os.environ.get('BOT_TOKEN')
        bot = TelegramBOT(BOT_TOKEN, database)

    finally:
        if connection is not None:
            connection.close()
