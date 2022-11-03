from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def get_full_tank_info(id):
    keyboard = [
        [
            InlineKeyboardButton('Подробнее', callback_data=id),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def format_tank_info(tank_info):
    return f"""<b>Номер ЦКТ:</b> {tank_info['tank_number']}
    <b>Сорт пива:</b> {tank_info['tank_title_value']}
    <b>Используемые дрожжи:</b> {tank_info['yeats']}
    <b>Пиво начало набирать давление:</b> {tank_info['tank_beer_grooving']}
    <b>Охлажденный:</b> {tank_info['tank_cooling']}
    <b>Ожидаемый объем:</b> {tank_info['tank_expected_volume']}
    <b>Реальный объем:</b> {tank_info['tank_actual_volume']}
    """
