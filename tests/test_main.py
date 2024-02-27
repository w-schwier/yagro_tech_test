from unittest.mock import patch

from factory_simulator import main
from factory_simulator.config import BELT_LENGTH, TICKS_TO_RUN, ASSEMBLY_TICKS


@patch('factory_simulator.main.input')
@patch('factory_simulator.main.Factory')
def test_main_can_run_stepped_simulation(mock_factory, mock_input):
    # GIVEN
    mock_factory.return_value = mock_factory
    belt_length = 3
    mock_input.side_effect = ['', '', 'c', '']
    # WHEN
    main.run_stepped_simulation(belt_length)
    # THEN
    mock_factory.assert_called_once_with(belt_length)
    assert mock_factory.tick.call_count == 2
    assert mock_factory.print_state.call_count == 2
    assert mock_input.call_count == 3
    mock_factory.print_tally.assert_called_once()


@patch('factory_simulator.main.Factory')
def test_main_can_run_set_tick_simulation(mock_factory):
    # GIVEN
    ticks_to_run = 10
    belt_length = 3
    mock_factory.return_value = mock_factory
    # WHEN
    main.run_set_tick_simulation(belt_length, ticks_to_run, False)
    # THEN
    mock_factory.assert_called_once_with(belt_length)
    assert mock_factory.tick.call_count == 10
    assert mock_factory.print_state.call_count == 0
    mock_factory.print_tally.assert_called_once()


@patch('factory_simulator.main.Factory')
def test_main_can_run_set_tick_simulation_verbose(mock_factory):
    # GIVEN
    ticks_to_run = 10
    belt_length = 3
    mock_factory.return_value = mock_factory
    # WHEN
    main.run_set_tick_simulation(belt_length, ticks_to_run, True)
    # THEN
    mock_factory.assert_called_once_with(belt_length)
    assert mock_factory.tick.call_count == 10
    assert mock_factory.print_state.call_count == 10
    mock_factory.print_tally.assert_called_once()


def test_main_can_get_config_from_defaults():
    # GIVEN
    belt_length = BELT_LENGTH
    ticks_to_run = TICKS_TO_RUN
    assembly_ticks = ASSEMBLY_TICKS
    # WHEN
    config = main.get_config(None, None, None)
    # THEN
    assert config["belt_length"] is belt_length
    assert config["ticks_to_run"] is ticks_to_run
    assert config["assembly_ticks"] is assembly_ticks


def test_main_can_get_config_overridden():
    # GIVEN
    belt_length = 5
    ticks_to_run = 10
    assembly_ticks = 10
    # WHEN
    config = main.get_config(belt_length, ticks_to_run, assembly_ticks)
    # THEN
    assert config["belt_length"] is belt_length
    assert config["ticks_to_run"] is ticks_to_run
    assert config["assembly_ticks"] is assembly_ticks


@patch('factory_simulator.main.run_stepped_simulation')
@patch('factory_simulator.main.get_config')
def test_main_can_run_stepped(mock_get_config, mock_run_stepped_simulation):
    # GIVEN
    belt_length = 2
    mock_get_config.return_value = {"belt_length": belt_length}
    # WHEN
    main.run(True, belt_length)
    # THEN
    mock_get_config.assert_called_once_with(belt_length, None, None)
    mock_run_stepped_simulation.assert_called_once_with(belt_length)


@patch('factory_simulator.main.run_set_tick_simulation')
@patch('factory_simulator.main.get_config')
def test_main_can_run_set_tick(mock_get_config, mock_run_set_tick_simulation):
    # GIVEN
    belt_length = 2
    ticks_to_run = 8
    mock_get_config.return_value = {"belt_length": belt_length, "ticks_to_run": ticks_to_run}
    # WHEN
    main.run(False, belt_length, ticks_to_run, None, True)
    # THEN
    mock_get_config.assert_called_once_with(belt_length, ticks_to_run, None)
    mock_run_set_tick_simulation.assert_called_once_with(belt_length, ticks_to_run, True)
