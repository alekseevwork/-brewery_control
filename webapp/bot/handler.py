from telegram import ParseMode
from webapp.bot.utils import get_full_tank_info
from webapp.tank.utils import create_diagrams_for_tanks


def view_tanks(update, context):
    chat_id = update.effective_chat.id
    diagram = create_diagrams_for_tanks()
    print(diagram)
    #update.message.reply_text(diagram, reply_markup=get_full_tank_info(), parse_mode=ParseMode.HTML)
