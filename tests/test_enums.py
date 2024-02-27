from enum import Flag, Enum

import pytest
from unittest.mock import patch
from factory_simulator.enums import Item, Row


def test_item_is_type_flag():
    assert issubclass(Item, Flag)


def test_row_is_type_enum():
    assert issubclass(Row, Enum)


def test_type_a_and_type_b_items_are_components():
    assert Item.A in Item.COMPONENT
    assert Item.B in Item.COMPONENT


@pytest.mark.parametrize(
    "item",
    [Item.EMPTY, Item.A, Item.B, Item.P, Item.COMPONENT]
)
def test_item_representation_is_the_items_name(item):
    # GIVEN
    expected = item.name
    # WHEN
    actual = repr(item)
    # THEN
    assert actual == expected


@patch('factory_simulator.enums.random.choice')
def test_item_returns_random_input(mock_random_choice):
    # GIVEN
    expected = Item.EMPTY
    mock_random_choice.return_value = expected
    # WHEN
    actual = Item.get_random_input()
    # THEN
    mock_random_choice.assert_called_once_with((expected, Item.A, Item.B))
    assert actual == expected
