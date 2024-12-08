from itertools import combinations

ALL_LETTERS = "abcdefghijklmnopqrstuvwxyz"
ALL_NUMBERS = "0123456789"
ALL_CHARS = ALL_LETTERS + ALL_LETTERS.upper() + ALL_NUMBERS


def read_data(data_file) -> list[list[str]]:
    with open(data_file, "r") as file:
        loaded_data = file.readlines()
    return [list(line.strip()) for line in loaded_data]


def find_antennas(data: list[list[str]]) -> dict[str, list[tuple[int, int]]]:
    antennas: dict = {}
    for i, row in enumerate(data):
        for j, char in enumerate(row):
            if char != ".":
                antennas.setdefault(char, []).append((i, j))
    return antennas


def find_aninodes(
    antennas: dict[str, list[tuple[int, int]]], max_x: int, max_y: int
) -> set[tuple[int, int]]:
    antinodes = set()
    for char, coords in antennas.items():
        for coord1, coord2 in combinations(coords, 2):
            vector = get_vector(coord1, coord2)
            antinode1 = coord2[0] + vector[0], coord2[1] + vector[1]
            antinode2 = coord1[0] - vector[0], coord1[1] - vector[1]
            if check_if_within_range(antinode1, max_x, max_y):
                antinodes.add(antinode1)
            if check_if_within_range(antinode2, max_x, max_y):
                antinodes.add(antinode2)
    return antinodes


def find_aninodes_with_harmonics(
    antennas: dict[str, list[tuple[int, int]]], max_x: int, max_y: int
) -> set[tuple[int, int]]:
    antinodes = set()
    for char, coords in antennas.items():
        for coord1, coord2 in combinations(coords, 2):
            antinodes.add(coord1)
            antinodes.add(coord2)
            vector = get_vector(coord1, coord2)
            i = 1
            while True:
                antinode1 = coord2[0] + (i * vector[0]), coord2[1] + (i * vector[1])
                if check_if_within_range(antinode1, max_x, max_y):
                    antinodes.add(antinode1)
                else:
                    break
                i += 1
            i = 1
            while True:
                antinode2 = coord1[0] - (i * vector[0]), coord1[1] - (i * vector[1])
                if check_if_within_range(antinode2, max_x, max_y):
                    antinodes.add(antinode2)
                else:
                    break
                i += 1
    return antinodes


def get_vector(coord1: tuple[int, int], coord2: tuple[int, int]) -> tuple[int, int]:
    """Get the vector from coord1 to coord2"""
    return coord2[0] - coord1[0], coord2[1] - coord1[1]


def check_if_within_range(coord: tuple[int, int], max_x: int, max_y: int) -> bool:
    return 0 <= coord[0] < max_x and 0 <= coord[1] < max_y


if __name__ == "__main__":
    data = read_data("day8\\input.txt")
    antennas = find_antennas(data)
    max_x, max_y = len(data), len(data[0])
    print(f"Max x: {max_x}, Max y: {max_y}")
    antinodes = find_aninodes(antennas, max_x, max_y)
    print(f"Number of antinodes: {len(antinodes)}")

    antinodes_with_harmonics = find_aninodes_with_harmonics(antennas, max_x, max_y)
    print(f"Number of antinodes with harmonics: {len(antinodes_with_harmonics)}")
