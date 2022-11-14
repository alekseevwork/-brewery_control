from enum import Enum


class TypeOfYeast(Enum):
    wb_06 = 'wb-06'
    k_97 = 'k-97'
    w_34_70 = 'w-34/70'
    maxifarm = 'maxifarm'

    def stock_name(self):
        name = {
            TypeOfYeast.w_34_70: 'Fermentis 34/70',
            TypeOfYeast.wb_06: 'Fermentis WB-06',
            TypeOfYeast.k_97: 'Fermentis K-97',
            TypeOfYeast.maxifarm: 'Fermentis SafCider',
        }
        return name[self]