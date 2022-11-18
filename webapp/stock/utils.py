from webapp.stock.enums import ProductType, ProductName
from webapp.stock.models import Stock
from webapp.tank.enums import TitleBeer

malt_range = [
    'Pilsner (SП) (40 кг.)',
    'Pilsner Premium (SП) (25 кг.)',
    'Pale Ale (SП) (40 кг.)',
    'Пшеничный (SП) (40 кг.)',
    'Мюнхенский (15 EBC) (SП) (40 кг.)',
    'Мюнхенский (25 EBC) (SП) (40 кг.)',
    'Жженый (1200-1400) (SП) (25 кг.)',
    'Cara Clair (6 EBC) (CM) (25 кг.)',
    'Melano (80 EBC) (CM) (25 кг.)',
    'Crystal (150 EBC) (CM) (25 кг.)',
]
hop_range = [
    'Cascade (HCA) (6,0)',
    'Mandarina (HMBA) (7,5)',
    'Mittelfruh (HHAL) (5,5)',
    'Nugget (HNUG) (11,3)',
    'Perle (HPER) (6,9)',
    'Sp. Select (HSSE) (5,2)',
]
yeasts_range = [
    'Fermentis 34/70',
    'Fermentis WB-06',
    'Fermentis K-97',
    'Fermentis SafCider',
]


def get_the_right_product(type):
    if type == ProductType.malt.name:
        return malt_range
    elif type == ProductType.hop.name:
        return hop_range
    elif type == ProductType.yeast.name:
        return yeasts_range
    else:
        return None
  

def get_needs_materials_for_brew_in_stock(title_beer, num_brew, num_tank):
    """amount material for brew tank"""
    quantity_of_materials = {}
    if title_beer == TitleBeer.kellerbier.value:
        malt = 215
        if num_tank > 19:
            malt = 220
        quantity_of_materials[ProductName.pils.value] = malt * num_brew
        quantity_of_materials[ProductName.munch25.value] = 25 * num_brew
        quantity_of_materials[ProductName.perle.value] = 0.35 * num_brew
        quantity_of_materials[ProductName.mandarina.value] = 0.35 * num_brew
        quantity_of_materials[ProductName.mittelfruh.value] = 0.5 * num_brew
    elif title_beer == TitleBeer.dunkelbier.value:
        pils, munhen, roasted  = 185, 20, 10 
        if num_tank > 3:
            pils, munhen, roasted  = 215, 25, 15 
        quantity_of_materials[ProductName.pils.value] = pils * num_brew
        quantity_of_materials[ProductName.munch25.value] = munhen * num_brew
        quantity_of_materials[ProductName.roasted.value] = roasted  * num_brew
        quantity_of_materials[ProductName.perle.value] = 0.35 * num_brew
        quantity_of_materials[ProductName.mandarina.value] = 0.35 * num_brew
        quantity_of_materials[ProductName.mittelfruh.value] = 0.5 * num_brew
    elif title_beer == TitleBeer.bropils.value:
        quantity_of_materials[ProductName.pilsPremium.value] = 215 * num_brew
        quantity_of_materials[ProductName.caraClair.value] = 12.5 * num_brew
        quantity_of_materials[ProductName.perle.value] = 1 * num_brew
        quantity_of_materials[ProductName.select.value] = 1 * num_brew
    elif title_beer == TitleBeer.wheatbeer.value:
        quantity_of_materials[ProductName.pils.value] = 75 * num_brew
        quantity_of_materials[ProductName.munch25.value] = 75 * num_brew
        quantity_of_materials[ProductName.wheat.value] = 100 * num_brew
        quantity_of_materials[ProductName.perle.value] = 0.5 * num_brew
    elif title_beer == TitleBeer.traditional_dark.value:
        quantity_of_materials[ProductName.pils.value] = 190 * num_brew
        quantity_of_materials[ProductName.munch15.value] = 25 * num_brew
        quantity_of_materials[ProductName.roasted.value] = 15 * num_brew
        quantity_of_materials[ProductName.perle.value] = 0.7 * num_brew
        quantity_of_materials[ProductName.select.value] = 0.8 * num_brew
    elif title_beer == TitleBeer.traditional_light.value:
        quantity_of_materials[ProductName.pils.value] = 190 * num_brew
        quantity_of_materials[ProductName.munch15.value] = 25 * num_brew
        quantity_of_materials[ProductName.caraClair.value] = 10 * num_brew
        quantity_of_materials[ProductName.perle.value] = 0.7 * num_brew
        quantity_of_materials[ProductName.select.value] = 0.8 * num_brew
    elif title_beer == TitleBeer.traditional_wheat.value:
        quantity_of_materials[ProductName.paleAle.value] = 115 * num_brew
        quantity_of_materials[ProductName.wheat.value] = 115 * num_brew
        quantity_of_materials[ProductName.mandarina.value] = 0.7 * num_brew
        quantity_of_materials[ProductName.cascade.value] = 0.8 * num_brew
    elif title_beer == TitleBeer.cider.value:
        quantity_of_materials[ProductName.pils.value] = 180 * num_brew
        quantity_of_materials[ProductName.nugget.value] = 115 * num_brew
    return quantity_of_materials


def is_stock_products(in_stock, need_stock):
    result = in_stock - need_stock
    if in_stock < need_stock:
        return True, -round(result, 2)
    return False, -round(result, 2)


def is_amount_yasts_in_stock(amount_yasts, name_yasts):
    try:
        amount_yasts_in_stock = Stock.query.filter(Stock.name_product==name_yasts).first().amount_product
        if amount_yasts_in_stock < amount_yasts:
            return False
        return True
    except AttributeError:
        return False
