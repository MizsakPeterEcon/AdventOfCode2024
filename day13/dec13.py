import re
from dataclasses import dataclass

import numpy as np

BUTTON_PATTERN = re.compile(r"Button [AB]: X([^,]+), Y([^,]+)")
PRIZE_PATTERN = re.compile(r"Prize: X=([^,]+), Y=([^,]+)")


@dataclass
class ClawMachine:
    A_button: tuple[int, int]
    B_button: tuple[int, int]
    price: tuple[int, int]

    @property
    def matrix(self):
        return np.array([self.A_button, self.B_button]).T

    @property
    def solution(self):
        return np.array(self.price)

    def calculate_solution(self):
        return np.linalg.solve(self.matrix, self.solution)

    def check_solution(self, res: np.ndarray):
        res = np.round(res).astype(int)
        if np.array_equal(np.dot(self.matrix, res), self.solution):
            return True
        return False

    def get_solution_cost(self, max_presses=100):
        res = self.calculate_solution()
        if max_presses:
            if res[0] > max_presses or res[1] > max_presses:
                return 0
        if self.check_solution(res):
            print(f"CORRECT SOLUTION: {res}")
            return res[0] * 3 + res[1]
        return 0


def read_data(data_file: str):
    machines = []
    with open(data_file, "r") as file:
        _loaded_data = file.readlines()
        _loaded_data = [line.strip() for line in _loaded_data]

        for idx in range(int(len(_loaded_data) / 4) + 1):
            button_a = BUTTON_PATTERN.match(_loaded_data[idx * 4])
            button_b = BUTTON_PATTERN.match(_loaded_data[idx * 4 + 1])
            prize = PRIZE_PATTERN.match(_loaded_data[idx * 4 + 2])
            assert button_a and button_b and prize, f"Invalid data at line {idx * 4}"
            cm = ClawMachine(
                A_button=(int(button_a.group(1)), int(button_a.group(2))),
                B_button=(int(button_b.group(1)), int(button_b.group(2))),
                price=(int(prize.group(1)), int(prize.group(2))),
            )
            machines.append(cm)
    return machines


if __name__ == "__main__":
    data = read_data("day13\\input.txt")
    print(data)
    total_cost = 0
    for cm in data:
        cost = cm.get_solution_cost()
        # print(f"Cost: {cost}")
        total_cost += cost
    print(f"Total cost: {total_cost}")

    # part2
    offset = 10000000000000
    total_cost = 0
    for cm in data:
        cm.price = (cm.price[0] + offset, cm.price[1] + offset)
        cost = cm.get_solution_cost(None)
        # print(f"Cost: {cost}")
        total_cost += cost
    print(f"Total cost: {total_cost}")
