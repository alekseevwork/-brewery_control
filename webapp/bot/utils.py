from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def get_full_tank_info():
    keyboard = [
        [
            InlineKeyboardButton('Подробнее', callback_data='Test'),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)
