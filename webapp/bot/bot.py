from os import environ
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler
from webapp.bot.handler import view_tanks
import logging

load_dotenv()

logging.basicConfig(filename='bot.log', level=logging.INFO, format='%(asctime)s %(message)s')


def main():
    bot = Updater(environ.get('BOT_API_KEY'))
    dp = bot.dispatcher
    
    dp.add_handler(CommandHandler('start', view_tanks))

    bot.start_polling()
    
    print('Bot started...')
    
    bot.idle()

if __name__ == '__main__':    
    main()
