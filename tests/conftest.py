import pytest

from factory_simulator.belt import Belt


@pytest.fixture(autouse=True, scope="function")
def reset_belt_slots():
    yield
    Belt().slots = []
