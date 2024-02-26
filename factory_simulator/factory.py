from collections import Counter
from typing import List

from factory_simulator.enums import Row
from factory_simulator.belt import Belt
from factory_simulator.worker import Worker


class Factory:
    def __init__(self, belt_length: int):
        self.belt: Belt = Belt()
        self.workers: dict = {Row.TOP: [], Row.BOTTOM: []}
        self.output: List = []
        self._set_up(belt_length)

    def _set_up(self, belt_length: int):
        while len(self.belt.slots) < belt_length:
            self.belt.add_empty_item()
            self.workers[Row.TOP].append(Worker(len(self.workers[Row.TOP]), Row.TOP))
            self.workers[Row.BOTTOM].append(Worker(len(self.workers[Row.BOTTOM]), Row.BOTTOM))
        print(f"Empty belt created with {belt_length} slot(s)\nWorkers populated")

    def _action_workers(self):
        for worker in self.workers[Row.TOP]:
            worker.take_action(self.belt)
        for worker in self.workers[Row.BOTTOM]:
            worker.take_action(self.belt)

    def tick(self):
        self.output.append(self.belt.move())
        self._action_workers()

    def print_state(self):
        top_row_workers = [f"{w.belt_position}: {w.held}" for w in self.workers[Row.TOP]]
        bottom_row_workers = [f"{w.belt_position}: {w.held}" for w in self.workers[Row.BOTTOM]]
        print(f"{Row.TOP.name}: {top_row_workers}")
        print(f"Belt: {self.belt.slots}")
        print(f"{Row.BOTTOM.name}: {bottom_row_workers}")
        print("\n***************\n")

    def print_tally(self):
        print(Counter(self.output))
