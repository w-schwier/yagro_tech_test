import random
from enum import Flag, Enum, auto


class Item(Flag):
    EMPTY = auto()
    TYPE_A = auto()
    TYPE_B = auto()
    PRODUCT = auto()
    COMPONENT = TYPE_A | TYPE_B
    INPUT = EMPTY | COMPONENT

    def __repr__(self):
        return self.name

    @classmethod
    def get_random_input(cls) -> INPUT:
        return random.choice((cls.EMPTY, cls.TYPE_A, cls.TYPE_B))


class Row(Enum):
    TOP = auto()
    BOTTOM = auto()
