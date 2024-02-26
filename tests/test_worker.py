from unittest.mock import patch, Mock

import pytest

from factory_simulator.belt import Belt
from factory_simulator.enums import Row, Item
from factory_simulator.worker import Worker


@pytest.fixture(autouse=True)
def reset_belt_slots():
    yield
    Belt().slots = []


def test_worker_is_initialised_correctly():
    # GIVEN
    belt_position = 2
    row = Row.TOP
    # WHEN
    worker = Worker(belt_position, row)
    # THEN
    assert worker.belt_position is belt_position
    assert worker.row is row
    assert len(worker.held) is 0
    assert worker.NUMBER_OF_HANDS is 2


def test_worker_can_place_product():
    # GIVEN
    belt = Belt()
    belt.add_empty_item()
    worker = Worker(0, Row.TOP)
    worker.held = [Item.PRODUCT]
    # WHEN
    action_taken = worker._place_product(belt)
    # THEN
    assert action_taken is True
    assert not worker.held
    assert belt.slots[0] is Item.PRODUCT


@pytest.mark.parametrize(
    "held",
    [[], [Item.TYPE_A], [Item.TYPE_B]]
)
def test_worker_cannot_place_product_when_they_do_not_have_one(held):
    # GIVEN
    belt = Belt()
    belt.add_empty_item()
    worker = Worker(0, Row.TOP)
    worker.held = held
    # WHEN
    action_taken = worker._place_product(belt)
    # THEN
    assert action_taken is False
    assert worker.held == held
    assert belt.slots[0] is Item.EMPTY


@pytest.mark.parametrize(
    "item",
    [[Item.PRODUCT], [Item.TYPE_A], [Item.TYPE_B]]
)
def test_worker_cannot_place_product_when_belt_solt_is_not_empty(item):
    # GIVEN
    belt = Belt()
    belt.add_empty_item().move(item)
    worker = Worker(0, Row.TOP)
    worker.held = [Item.PRODUCT]
    # WHEN
    action_taken = worker._place_product(belt)
    # THEN
    assert action_taken is False
    assert worker.held == [Item.PRODUCT]
    assert belt.slots[0] is item


def test_worker_can_pick_up_component():
    # GIVEN
    belt = Belt()
    belt.add_empty_item().move(Item.TYPE_A)
    worker = Worker(0, Row.TOP)
    worker.held = []
    # WHEN
    action_taken = worker._pick_up_component(belt)
    # THEN
    assert action_taken is True
    assert worker.held == [Item.TYPE_A]
    assert belt.slots[0] is Item.EMPTY


def test_worker_cannot_pick_up_component_when_hands_full():
    # GIVEN
    belt = Belt()
    belt.add_empty_item().move(Item.TYPE_A)
    worker = Worker(0, Row.TOP)
    held = [Item.PRODUCT, Item.TYPE_B]
    worker.held = held
    # WHEN
    action_taken = worker._pick_up_component(belt)
    # THEN
    assert action_taken is False
    assert worker.held == held
    assert belt.slots[0] is Item.TYPE_A


@pytest.mark.parametrize(
    "item",
    [Item.PRODUCT, Item.EMPTY]
)
def test_worker_cannot_pick_up_component_when_belt_slot_item_is_not_a_component(item):
    # GIVEN
    belt = Belt()
    belt.add_empty_item().move(item)
    worker = Worker(0, Row.TOP)
    held = [Item.TYPE_B]
    worker.held = held
    # WHEN
    action_taken = worker._pick_up_component(belt)
    # THEN
    assert action_taken is False
    assert worker.held == held
    assert belt.slots[0] is item


@pytest.mark.parametrize(
    "item",
    [Item.TYPE_A, Item.TYPE_B]
)
def test_worker_cannot_pick_up_component_when_already_held(item):
    # GIVEN
    belt = Belt()
    belt.add_empty_item().move(item)
    worker = Worker(0, Row.TOP)
    held = [item]
    worker.held = held
    # WHEN
    action_taken = worker._pick_up_component(belt)
    # THEN
    assert action_taken is False
    assert worker.held == held
    assert belt.slots[0] is item


def test_worker_can_assemble():
    # GIVEN
    worker = Worker(0, Row.TOP)
    worker.held = [Item.TYPE_A, Item.TYPE_B]
    # WHEN
    action_taken = worker._assemble()
    # THEN
    assert action_taken is True
    assert worker.held == [Item.PRODUCT]


@pytest.mark.parametrize(
    "held",
    [[], [Item.TYPE_A], [Item.TYPE_B], [Item.PRODUCT], [Item.PRODUCT, Item.TYPE_A], [Item.PRODUCT, Item.TYPE_B]]
)
def test_worker_cannot_assemble_without_all_components(held):
    # GIVEN
    worker = Worker(0, Row.TOP)
    worker.held = held
    # WHEN
    action_taken = worker._assemble()
    # THEN
    assert action_taken is False
    assert worker.held is held


@patch.object(Worker, '_assemble', return_value=False)
@patch.object(Worker, '_pick_up_component', return_value=False)
@patch.object(Worker, '_place_product', return_value=True)
def test_worker_takes_action_to_place_product(mock_place_product, mock_pick_up_component, mock_assemble):
    # GIVEN
    belt = Mock()
    worker = Worker(0, Row.TOP)
    # WHEN
    action_taken = worker.take_action(belt)
    # THEN
    assert action_taken is True
    mock_place_product.assert_called_once_with(belt)
    mock_pick_up_component.assert_not_called()
    mock_assemble.assert_not_called()


@patch.object(Worker, '_assemble', return_value=False)
@patch.object(Worker, '_pick_up_component', return_value=True)
@patch.object(Worker, '_place_product', return_value=False)
def test_worker_takes_action_to_pick_up_component(mock_place_product, mock_pick_up_component, mock_assemble):
    # GIVEN
    belt = Mock()
    worker = Worker(0, Row.TOP)
    # WHEN
    action_taken = worker.take_action(belt)
    # THEN
    assert action_taken is True
    mock_place_product.assert_called_once_with(belt)
    mock_pick_up_component.assert_called_once_with(belt)
    mock_assemble.assert_not_called()


@patch.object(Worker, '_assemble', return_value=True)
@patch.object(Worker, '_pick_up_component', return_value=False)
@patch.object(Worker, '_place_product', return_value=False)
def test_worker_takes_action_to_assemble(mock_place_product, mock_pick_up_component, mock_assemble):
    # GIVEN
    belt = Mock()
    worker = Worker(0, Row.TOP)
    # WHEN
    action_taken = worker.take_action(belt)
    # THEN
    assert action_taken is True
    mock_place_product.assert_called_once_with(belt)
    mock_pick_up_component.assert_called_once_with(belt)
    mock_assemble.assert_called_once()


@patch.object(Worker, '_assemble', return_value=False)
@patch.object(Worker, '_pick_up_component', return_value=False)
@patch.object(Worker, '_place_product', return_value=False)
def test_worker_takes_no_action(mock_place_product, mock_pick_up_component, mock_assemble):
    # GIVEN
    belt = Mock()
    worker = Worker(0, Row.TOP)
    # WHEN
    action_taken = worker.take_action(belt)
    # THEN
    assert action_taken is False
    mock_place_product.assert_called_once_with(belt)
    mock_pick_up_component.assert_called_once_with(belt)
    mock_assemble.assert_called_once()

