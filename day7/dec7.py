from itertools import product
from operator import add, mul

# OPERATORS = {"+": add, "*": mul}
OPERATORS = {"+": add, "*": mul, "||": lambda x, y: int(str(x) + str(y))}
POSSIBLE_OPERATORS = list(OPERATORS.keys())


def read_data(data_file) -> list[str]:
    with open(data_file, "r") as file:
        loaded_data = file.readlines()
    return [line.strip() for line in loaded_data]


def prepare_data(loaded_data: list[str]) -> list[tuple[int, list[int]]]:
    equations = []
    for row in loaded_data:
        res, nums_ = row.split(":")
        nums = nums_.strip().split()
        equations.append((int(res), [int(num) for num in nums]))

    return equations


def make_equation_true(res: int, nums: list[int]) -> bool:
    slots = len(nums) - 1
    for ops in product(POSSIBLE_OPERATORS, repeat=slots):
        val = nums[0]
        for idx, op in enumerate(ops, start=1):
            val = OPERATORS[op](val, nums[idx])
            if val > res:
                break
        if val == res:
            return True
    return False


def solve(equations: list[tuple[int, list[int]]]) -> int:
    solved_sum = 0
    for idx, (res, nums) in enumerate(equations):
        print(f"working on eq: {idx}")
        if make_equation_true(res, nums):
            solved_sum += res
    return solved_sum


if __name__ == "__main__":
    data = read_data("day7\\input.txt")
    prepared_data = prepare_data(data)
    # print(prepared_data)
    solved_sum = solve(prepared_data)
    print(f"Solved_sum: {solved_sum}")
