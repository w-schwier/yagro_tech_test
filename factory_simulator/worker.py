from factory_simulator.belt import Belt
from factory_simulator.enums import Item, Row


class Worker:
    NUMBER_OF_HANDS = 2

    def __init__(self, belt_position: int, row: Row):
        self.belt_position = belt_position
        self.row = row
        self.held = []

    def _can_place_product(self, belt: Belt) -> bool:
        return Item.P in self.held and belt.slots[self.belt_position] is Item.EMPTY

    def _can_pick_up_component(self, item: Item) -> bool:
        return len(self.held) < self.NUMBER_OF_HANDS and item in Item.COMPONENT and item not in self.held

    def _can_assemble(self) -> bool:
        return Item.A in self.held and Item.B in self.held

    def _place_product(self, belt: Belt) -> bool:
        if self._can_place_product(belt):
            belt.slots[self.belt_position] = self.held.pop(self.held.index(Item.P))
            return True
        return False

    def _pick_up_component(self, belt: Belt) -> bool:
        item = belt.slots[self.belt_position]
        if self._can_pick_up_component(item):
            self.held.append(item)
            belt.slots[self.belt_position] = Item.EMPTY
            return True
        return False

    def _assemble(self) -> bool:
        if self._can_assemble():
            self.held = [Item.P]
            return True
        return False

    def take_action(self, belt: Belt) -> bool:
        if self._place_product(belt):
            return True
        elif self._pick_up_component(belt):
            return True
        elif self._assemble():
            return True
        else:
            return False
