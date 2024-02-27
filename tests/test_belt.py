from unittest.mock import patch

from factory_simulator.belt import Belt
from factory_simulator.enums import Item


def test_belt_is_singleton():
    # GIVEN
    belt = Belt()
    # WHEN
    new_belt = Belt()
    # THEN
    assert belt is new_belt


def test_belt_slots_are_shared_across_variables():
    # GIVEN
    belt = Belt()
    new_belt = Belt()
    belt.slots.append(Item.A)
    # WHEN
    new_belt.slots.append(Item.B)
    # THEN
    assert belt.slots == new_belt.slots


def test_belt_can_add_empty_item():
    # GIVEN
    belt = Belt()
    # WHEN
    returned_belt = belt.add_empty_item()
    # THEN
    assert returned_belt is belt
    assert belt.slots[0] is Item.EMPTY


def test_belt_can_move():
    # GIVEN
    belt = Belt()
    belt.slots = [Item.EMPTY, Item.EMPTY, Item.P]
    # WHEN
    output = belt.move(Item.A)
    # THEN
    assert output is Item.P
    assert belt.slots[0] is Item.A


@patch.object(Item, 'get_random_input', return_value=Item.A)
def test_belt_can_move_using_random_input_as_default(mock_get_random_input):
    # GIVEN
    belt = Belt()
    belt.slots = [Item.EMPTY, Item.EMPTY, Item.P]
    # WHEN
    output = belt.move()
    # THEN
    mock_get_random_input.assert_called_once()
    assert output is Item.P
    assert belt.slots[0] is Item.A
