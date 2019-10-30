from enum import Enum, unique


@unique
class OilFieldStatusEnum(Enum):
    IDLE = 1
    DRILLING = 2
    FLOWING = 3
    PUMPING = 4
    EMPTY = 5
