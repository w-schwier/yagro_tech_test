import random
from enum import Flag, Enum, auto


class Item(Flag):
    EMPTY = auto()
    A = auto()  # Component A
    B = auto()  # Component B
    P = auto()  # Assembled Product
    COMPONENT = A | B
    INPUT = EMPTY | COMPONENT

    def __repr__(self):
        return self.name

    @classmethod
    def get_random_input(cls) -> INPUT:
        return random.choice((cls.EMPTY, cls.A, cls.B))


class Row(Enum):
    TOP = auto()
    BOTTOM = auto()
