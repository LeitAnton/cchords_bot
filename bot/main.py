import bot
import sqlite3
from database import Database


if __name__ == '__main__':
    try:
        connection = sqlite3.connect("../database.sqlite")
        cursor = connection.cursor()

        database = Database(connection, cursor)
        database.create_tables()

        bot
    finally:
        connection.close()
