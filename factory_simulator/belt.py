from typing import Optional, List
from typing_extensions import Self

from factory_simulator.enums import Item


class Belt(object):
    _instance: Optional[Self] = None
    slots: List[Item] = []

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Belt, cls).__new__(cls)
        return cls._instance

    def add_empty_item(self) -> Self:
        self.slots.append(Item.EMPTY)
        return self

    def move(self, item_to_add: Item = None) -> Item:
        if not item_to_add:
            item_to_add = Item.get_random_input()
        self.slots.insert(0, item_to_add)
        return self.slots.pop()
