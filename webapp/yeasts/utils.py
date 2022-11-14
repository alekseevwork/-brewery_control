from webapp.yeasts.enums import TypeOfYeast
from webapp.tank.enums import TitleBeer
from webapp.yeasts.models import Yeasts


def get_the_right_yeasts(beer_name):
    try:
        type_of_beer = TitleBeer[beer_name]
        yeast_34_70 = [
            TitleBeer.kellerbier,
            TitleBeer.dunkelbier,
            TitleBeer.bropils,
            TitleBeer.traditional_light,
            TitleBeer.traditional_dark]
        if type_of_beer in yeast_34_70:
            return TypeOfYeast.w_34_70
        elif type_of_beer == TitleBeer.wheatbeer:
            return TypeOfYeast.wb_06
        elif type_of_beer == TitleBeer.traditional_wheat:
            return TypeOfYeast.k_97
        elif type_of_beer == TitleBeer.cider:
            return TypeOfYeast.maxifarm
    except KeyError:
        pass


def is_the_generation_suitable(type_yeast, generate_yeast):
    if type_yeast != TypeOfYeast.w_34_70 and generate_yeast >= 1:
        return False
    if generate_yeast >= 6:
        return False
    else:
        return True


def get_list_of_suitable_tanks(yeasts):
    list_tanks = []
    yeastObjects = Yeasts.query.filter(Yeasts.name == yeasts)
    for yeast in yeastObjects:
        tanks = yeast.tanks
        if tanks:
            if is_the_generation_suitable(yeast.name, yeast.cycles):
                for tank in tanks:
                    if tank.cooling:
                        list_tanks.append([f'#{tank.number} {tank.title.product_name()} др. {yeast.name.value} ген. {yeast.cycles}-я  /{yeast.id}'])
    return list_tanks


def get_id_now_yeast(info_for_yeats):
    positions_id = info_for_yeats.rfind('/') + 1
    try:
        yeast_id = int(info_for_yeats[positions_id:])
    except ValueError:
        return -1, -1
    positions = info_for_yeats.rfind('-') - 1
    try:
        generation = int(info_for_yeats[positions])
    except IndexError:
        return yeast_id, 0
    return yeast_id, generation


def get_need_yasts(name_yasts, numbers_brew):
    amount_yeast = 0.5
    if name_yasts == TypeOfYeast.wb_06 or name_yasts == TypeOfYeast.k_97:
        if numbers_brew > 2:
            amount_yeast = 1
    elif name_yasts == TypeOfYeast.w_34_70:
        amount_yeast = 1
        if numbers_brew > 2:
            amount_yeast = 1.5
    elif name_yasts == TypeOfYeast.maxifarm:
        amount_yeast = 1
    return amount_yeast
