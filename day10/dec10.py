DIRS = [(1, 0), (0, -1), (-1, 0), (0, 1)]


def read_data(data_file: str) -> list[list[int]]:
    with open(data_file, "r") as file:
        _loaded_data = file.readlines()
    return [[int(n) for n in line.strip()] for line in _loaded_data]


def find_trail_heads(data: list[list[int]]) -> list[tuple[int, int]]:
    return [
        (row_idx, col_idx)
        for row_idx, row in enumerate(data)
        for col_idx, val in enumerate(row)
        if val == 0
    ]


def find_trails(data: list[list[int]], start: tuple[int, int]):
    found_ends: set[tuple[int, int]] = set()
    found_trails = [0]
    do_steps(data, start, found_ends, found_trails)
    return found_ends, found_trails[0]


def do_steps(
    data: list[list[int]],
    from_pos: tuple[int, int],
    found_ends: set[tuple[int, int]],
    found_trails=list[int],
):

    current_value = data[from_pos[0]][from_pos[1]]
    next_value = current_value + 1
    for d in DIRS:
        next_pos = (from_pos[0] + d[0], from_pos[1] + d[1])
        if next_pos[0] < 0 or next_pos[1] < 0:
            continue
        try:
            if data[next_pos[0]][next_pos[1]] == next_value:
                if next_value == 9:
                    found_ends.add(next_pos)
                    found_trails[0] += 1
                do_steps(data, next_pos, found_ends, found_trails)
        except IndexError:
            continue


if __name__ == "__main__":
    data = read_data("day10\\input.txt")
    print(data)
    trail_heads = find_trail_heads(data)
    print(trail_heads)
    all_ends = 0
    all_trails = 0
    for trail_head in trail_heads:
        found_ends, found_trails = find_trails(data, trail_head)
        # print(f"Started at {trail_head}. Found ends: {found_ends}")
        all_ends += len(found_ends)
        # print(f"Found trails: {found_trails}")
        all_trails += found_trails
    print(f"Total ends found: {all_ends}")
    print(f"Total trails found: {all_trails}")
