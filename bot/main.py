import os
import sqlite3
from database import Database
from parser import Parser
from bot import TelegramBOT


if __name__ == '__main__':
    try:
        connection = sqlite3.connect("../database.sqlite", check_same_thread=False)
        cursor = connection.cursor()

        database = Database(connection, cursor)
        database.create_tables()

        parser = Parser(database)

        BOT_TOKEN = os.environ.get('BOT_TOKEN')
        bot = TelegramBOT(BOT_TOKEN, database, parser)
    finally:
        connection.close()
