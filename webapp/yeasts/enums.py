from enum import Enum


class TypeOfYeast(Enum):
    wb_06 = 'wb-06'
    k_97 = 'k-97'
    w_34_70 = 'w-34/70'
    maxifarm = 'maxifarm'

    @classmethod
    def list_names(cls):
        return [(role, name.value) for role, name in cls.__members__.items()]
        
