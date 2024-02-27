import argparse
from factory_simulator import main as factorio


def main():
    # Get command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--is-verbose", action="store_true",
                        help="Whether the state of the factory should be printed every tick - No effect on stepped run")
    parser.add_argument("-s", "--is-stepped", action="store_true",
                        help="Whether to run a simulation with the ability to manually step through it,"
                             "tick by tick")
    parser.add_argument("-b", "--belt-length", type=int,
                        help="How many slots the belt has, and consequentially, how many pairs of workers there are")
    parser.add_argument("-t", "--ticks", type=int,
                        help="How many ticks the simulation should run for - No effect on stepped run")
    parser.add_argument("-a", "--assembly-ticks", type=int,
                        help="How many ticks it takes to assemble a product - Not yet fully implemented in module")
    args = parser.parse_args()

    # Run the simulation, passing along command line arguments
    factorio.run(args.is_stepped, args.belt_length, args.ticks, args.assembly_ticks, args.is_verbose)


if __name__ == "__main__":
    main()
