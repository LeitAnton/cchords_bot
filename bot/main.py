import os
import sqlite3
from database import Database, create_tables
from parser import Parser
from bot import TelegramBOT

if __name__ == '__main__':
    try:
        connection = sqlite3.connect("../database.sqlite", check_same_thread=False)
        cursor = connection.cursor()

        create_tables(connection, cursor)
        database = Database(connection, cursor)

        parser = Parser()

        BOT_TOKEN = os.environ.get('BOT_TOKEN')
        bot = TelegramBOT(BOT_TOKEN, database, parser)

    finally:
        connection.close()
