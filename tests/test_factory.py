from unittest.mock import patch, Mock

from factory_simulator.belt import Belt
from factory_simulator.enums import Row, Item
from factory_simulator.factory import Factory
from factory_simulator.worker import Worker


@patch.object(Factory, '_set_up')
def test_factory_is_initialised_correctly(mock_set_up):
    # GIVEN
    belt_length = 3
    belt = Belt()
    # WHEN
    factory = Factory(belt_length)
    # THEN
    assert factory.belt is belt
    assert factory.workers == {Row.TOP: [], Row.BOTTOM: []}
    assert factory.output == []
    mock_set_up.assert_called_once_with(belt_length)


def test_factory_can_be_set_up(capfd):
    # GIVEN
    belt_length = 1
    factory = Factory(0)
    # WHEN
    # The next line clear's the printed text generated on factory creation (same further down)
    capfd.readouterr()
    factory._set_up(belt_length)
    out, err = capfd.readouterr()
    # THEN
    assert factory.belt.slots == [Item.EMPTY]
    assert len(factory.workers[Row.TOP]) is 1
    assert len(factory.workers[Row.BOTTOM]) is 1
    assert isinstance(factory.workers[Row.TOP][0], Worker)
    assert isinstance(factory.workers[Row.BOTTOM][0], Worker)
    assert out == "Empty belt created with 1 slot(s)\nWorkers populated\n"


def test_factory_can_action_workers():
    # GIVEN
    belt = Belt()
    top_worker1 = Mock()
    top_worker2 = Mock()
    bottom_worker1 = Mock()
    bottom_worker2 = Mock()
    top_worker1.take_action.return_value = False
    top_worker2.take_action.return_value = False
    bottom_worker1.take_action.return_value = True
    bottom_worker2.take_action.return_value = True
    factory = Factory(2)
    factory.workers = {Row.TOP: [top_worker1, top_worker2], Row.BOTTOM: [bottom_worker1, bottom_worker2]}
    # WHEN
    factory._action_workers()
    # THEN
    top_worker1.take_action.assert_called_once_with(belt)
    top_worker2.take_action.assert_called_once_with(belt)
    bottom_worker1.take_action.assert_called_once_with(belt)
    bottom_worker2.take_action.assert_called_once_with(belt)


def test_factory_only_has_one_belt_interaction_per_worker_pair_during_action_workers():
    # GIVEN
    belt = Belt()
    top_worker1 = Mock()
    top_worker2 = Mock()
    bottom_worker1 = Mock()
    bottom_worker2 = Mock()
    top_worker1.take_action.return_value = False
    top_worker2.take_action.return_value = True
    bottom_worker1.take_action.return_value = True
    bottom_worker2.take_action.return_value = False
    factory = Factory(2)
    factory.workers = {Row.TOP: [top_worker1, top_worker2], Row.BOTTOM: [bottom_worker1, bottom_worker2]}
    # WHEN
    factory._action_workers()
    # THEN
    top_worker1.take_action.assert_called_once_with(belt)
    top_worker2.take_action.assert_called_once_with(belt)
    bottom_worker1.take_action.assert_called_once_with(belt)
    bottom_worker2.take_action.assert_not_called()


@patch.object(Factory, '_action_workers')
@patch.object(Belt, 'move')
def test_factory_can_tick(mock_move_belt, mock_action_workers):
    # GIVEN
    item = Item.P
    factory = Factory(1)
    mock_move_belt.return_value = item
    # WHEN
    factory.tick()
    # THEN
    assert factory.output == [item]
    mock_move_belt.assert_called_once()
    mock_action_workers.assert_called_once()


def test_factory_can_print_state(capfd):
    # GIVEN
    top_worker = Worker(0, Row.TOP)
    bottom_worker = Worker(0, Row.BOTTOM)
    top_worker.held = [Item.P]
    bottom_worker.held = [Item.A, Item.B]
    factory = Factory(1)
    factory.workers = {Row.TOP: [top_worker], Row.BOTTOM: [bottom_worker]}
    expected_text = (
        "TOP ROW: ['1: [P]']\n"
        "BELT: ['1: [EMPTY]']\n"
        "BOTTOM ROW: ['1: [A, B]']\n"
        '\n'
        '***************\n'
        '\n'
    )
    # WHEN
    capfd.readouterr()
    factory.print_state()
    out, err = capfd.readouterr()
    # THEN
    assert out == expected_text


def test_factory_can_print_tally(capfd):
    # GIVEN
    factory = Factory(1)
    output = [Item.EMPTY, Item.EMPTY, Item.P, Item.A]
    factory.output = output
    expected_tally = "{EMPTY: 2, P: 1, A: 1}"
    # WHEN
    capfd.readouterr()
    factory.print_tally()
    out, err = capfd.readouterr()
    # THEN
    assert expected_tally in out
