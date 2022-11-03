from os import environ
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from handlers import view_full_tank_info, view_tanks
import logging

load_dotenv()

logging.basicConfig(filename='bot.log', level=logging.INFO, format='%(asctime)s %(message)s')


def main():
    bot = Updater(environ.get('BOT_API_KEY'))
    dp = bot.dispatcher
    
    dp.add_handler(CommandHandler('start', view_tanks))
    dp.add_handler(CallbackQueryHandler(view_full_tank_info))

    bot.start_polling()
    
    print('Bot started...')
    
    bot.idle()

if __name__ == '__main__':    
    main()