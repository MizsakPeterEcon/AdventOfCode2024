from copy import deepcopy
from dataclasses import dataclass

DIRECTION = {"^": (-1, 0), ">": (0, 1), "v": (1, 0), "<": (0, -1)}
PATH_MARKER = {"^": "|", ">": "-", "v": "|", "<": "-"}
MARKERS = list(DIRECTION.keys())


@dataclass
class Position:
    row: int
    col: int


def read_data(data_file) -> list[list[str]]:
    with open(data_file, "r") as file:
        loaded_data = file.readlines()
    return [list(line.strip()) for line in loaded_data]


def find_guard(data: list[list[str]]) -> tuple[Position, str]:
    for row_idx, row in enumerate(data):
        for col_idx, val in enumerate(row):
            if val in MARKERS:
                return Position(row_idx, col_idx), val
    raise ValueError("No guard found")


def get_value(data: list[list[str]], pos: Position) -> str:
    if pos.row < 0 or pos.col < 0:
        print(f"Out of bounds: {pos}")
        raise IndexError("Out of bounds")
    return data[pos.row][pos.col]


def set_value(data: list[list[str]], pos: Position, value: str):
    data[pos.row][pos.col] = value


def move_guard(pos: Position, direction: str, data: list[list[str]]):
    covered_path = []
    while True:
        move_direction = DIRECTION[direction]
        new_pos = Position(pos.row + move_direction[0], pos.col + move_direction[1])
        val = get_value(data, pos)

        if (pos, direction) in covered_path:
            # print("Loop closed at", pos, direction)
            raise ValueError("Loop found")

        if val == ".":
            set_value(data, pos, PATH_MARKER[direction])
            covered_path.append((pos, direction))
        elif val == "|" and PATH_MARKER[direction] == "-":
            set_value(data, pos, "+")
        elif val == "-" and PATH_MARKER[direction] == "|":
            set_value(data, pos, "+")

        try:
            new_val = get_value(data, new_pos)
        except IndexError:
            break

        if new_val == "#":
            direction = MARKERS[(MARKERS.index(direction) + 1) % len(MARKERS)]
            continue
        pos = new_pos
    return covered_path


def find_loops(
    data: list[list[str]],
    covered_path: list[tuple[Position, str]],
    init_pos: Position,
    init_dir: str,
):
    loop_positions = []
    all_possible_obstacles = len(covered_path)

    for idx, (pos, _dir) in enumerate(covered_path):
        modified_data = deepcopy(data)
        print(f"Checking loop with obstacle at {pos}, {idx}/{all_possible_obstacles}")
        modified_data[pos.row][pos.col] = "#"
        if idx > 0:
            init_pos, init_dir = covered_path[idx - 1]
        try:
            move_guard(init_pos, init_dir, modified_data)
        except ValueError:
            loop_positions.append(pos)

    return loop_positions


if __name__ == "__main__":
    data = read_data("day6\\input.txt")
    # print(data)
    init_pos, init_dir = find_guard(data)
    print(init_pos, init_dir)
    covered_path = move_guard(init_pos, init_dir, deepcopy(data))
    # print(covered_path)
    with open("day6\\covered_position_mp.txt", "w") as f:
        f.writelines(
            [f"({pos.row}, {pos.col}, {dir_})\n" for pos, dir_ in covered_path]
        )
    # +1 for the starting field
    print(f"The guard covered {len(covered_path)+1} fields")

    loop_positions = find_loops(data, covered_path, init_pos, init_dir)
    print(loop_positions)
    print(f"Number of new infinite loops: {len(loop_positions)}")
