from aiogram import Bot, Dispatcher
from database.database import Database

token = '7767420728:AAEeNQ8IBZgJ4n2ZD2xxVyPZ9xMhP3-IRmw'
bot = Bot(token=token)
dp = Dispatcher()
database = Database('db.sqlite3')