from factory_simulator.config import BELT_LENGTH, TICKS_TO_RUN, ASSEMBLY_TICKS
from factory_simulator.factory import Factory


def run_stepped_simulation(belt_length: int):
    factory = Factory(belt_length)
    cancel = input("What do you want to do? Press enter to step through to the next tick, or any other input to exit\n")
    while not cancel:
        factory.tick()
        factory.print_state()
        cancel = input("What do you want to do now? Same options as before!\n")
    factory.print_tally()


def run_set_tick_simulation(belt_length: int, ticks_to_run: int, is_verbose: bool = False):
    factory = Factory(belt_length)
    print("Running...")
    ticks = 0
    while ticks < ticks_to_run:
        factory.tick()
        ticks += 1
        if is_verbose:
            factory.print_state()
    print("Finished")
    factory.print_tally()


def get_config(belt_length: int = None, ticks_to_run: int = None, assembly_ticks: int = None) -> dict:
    belt_length = belt_length or BELT_LENGTH
    ticks_to_run = ticks_to_run or TICKS_TO_RUN
    assembly_ticks = assembly_ticks or ASSEMBLY_TICKS
    return {"belt_length": belt_length, "ticks_to_run": ticks_to_run, "assembly_ticks": assembly_ticks}


def run(
        is_stepped: bool = False,
        belt_length: int = None,
        ticks_to_run: int = None,
        assembly_ticks: int = None,
        is_verbose: bool = False
):
    config = get_config(belt_length, ticks_to_run, assembly_ticks)
    if is_stepped:
        run_stepped_simulation(config["belt_length"])
    else:
        run_set_tick_simulation(config["belt_length"], config["ticks_to_run"], is_verbose)
