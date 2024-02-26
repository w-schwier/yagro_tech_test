from factory_simulator.belt import Belt
from factory_simulator.enums import Item, Row


class Worker:
    NUMBER_OF_HANDS = 2

    def __init__(self, belt_position: int, row: Row):
        self.belt_position = belt_position
        self.row = row
        self.held = []

    def _place_product(self, belt: Belt) -> bool:
        if Item.PRODUCT in self.held and belt.slots[self.belt_position] is Item.EMPTY:
            belt.slots[self.belt_position] = self.held.pop(self.held.index(Item.PRODUCT))
            return True
        return False

    def _pick_up_component(self, belt: Belt) -> bool:
        item = belt.slots[self.belt_position]
        if len(self.held) < self.NUMBER_OF_HANDS and item in Item.COMPONENT and item not in self.held:
            self.held.append(item)
            belt.slots[self.belt_position] = Item.EMPTY
            return True
        return False

    def _assemble(self) -> bool:
        if Item.TYPE_A in self.held and Item.TYPE_B in self.held:
            self.held = [Item.PRODUCT]
            return True
        return False

    def take_action(self, belt: Belt) -> bool:
        if self._place_product(belt):
            return True
        if self._pick_up_component(belt):
            return True
        if self._assemble():
            return True
        return False
