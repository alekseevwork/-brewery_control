from enum import Enum

class ProductType(Enum):
    malt = 'malt'
    hop = 'hop'
    yeast = 'yeast'

    def translate_name(self):
        types = {
            ProductType.malt: 'Солод',
            ProductType.hop: 'Хмель',
            ProductType.yeast: 'Дрожжи'
        }
        return types[self]


class ProductName(Enum):
    pils = 'Pilsner (SП) (40 кг.)'
    pilsPremium = 'Pilsner Premium (SП) (25 кг.)'
    paleAle = 'Pale Ale (SП) (40 кг.)'
    wheat = 'Пшеничный (SП) (40 кг.)'
    munch15 = 'Мюнхенский (15 EBC) (SП) (40 кг.)'
    munch25 = 'Мюнхенский (25 EBC) (SП) (40 кг.)'
    roasted = 'Жженый (1200-1400) (SП) (25 кг.)'
    caraClair = 'Cara Clair (6 EBC) (CM) (25 кг.)'
    melano = 'Melano (80 EBC) (CM) (25 кг.)'
    crystal = 'Crystal (150 EBC) (CM) (25 кг.)'
    cascade = 'Cascade (HCA) (6,0)'
    mandarina = 'Mandarina (HMBA) (7,5)'
    mittelfruh = 'Mittelfruh (HHAL) (5,5)'
    nugget = 'Nugget (HNUG) (11,3)'
    perle = 'Perle (HPER) (6,9)'
    select = 'Sp. Select (HSSE) (5,2)'
