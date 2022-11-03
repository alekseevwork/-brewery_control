import requests
from os import environ
from dotenv import load_dotenv
from base64 import b64decode
from telegram import ParseMode
from utils import format_tank_info, get_full_tank_info

load_dotenv()
URL = environ.get('BOT_API_KEY')


def view_tanks(update, context):
    chat_id = update.effective_chat.id
    response = requests.get(f'{URL}/tanks-view')
    diagrams = response.json()
    for diagram in diagrams['diagrams']:
        image_code = diagrams['diagrams'].get(diagram)
        with open("diagram.png", "wb") as fh:
            fh.write(b64decode(image_code[22:]))
        context.bot.send_photo(chat_id=chat_id, photo=open('diagram.png', 'rb'), reply_markup=get_full_tank_info(diagram))


def view_full_tank_info(update, context):
    update.callback_query.answer()
    params = {
        'tank_id': update.callback_query.data
        }
    response = requests.get(f'{URL}/tanks-info', params=params)
    tank_info = response.json()
    update.callback_query.edit_message_caption(caption=format_tank_info(tank_info), parse_mode=ParseMode.HTML)