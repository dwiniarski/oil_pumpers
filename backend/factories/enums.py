from enum import Enum, unique


@unique
class FactoryTypeEnum(Enum):
    DRILL_FACTORY = 1
    PUMP_FACTORY = 2
    PIPE_FACTORY = 3
    WAGON_FACTORY = 4
    STORAGE_TANK_FACTORY = 5


@unique
class FactoryStateEnum(Enum):
    NON_OPERATIONAL = 1
    OPERATIONAL = 2
