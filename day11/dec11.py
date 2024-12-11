from functools import cache, lru_cache


def read_data(data_file: str) -> list[str]:
    with open(data_file, "r") as file:
        _loaded_data = file.read()
    return _loaded_data.strip().split(" ")


# not used any more
def blink_1_stone(data: list[str]) -> list[str]:
    to_insert = []
    for i, value in enumerate(data):
        if value == "0":
            data[i] = "1"
        elif len(value) % 2 == 1:
            data[i] = str(int(value) * 2024)
        else:
            data_len = len(value)
            half_len = data_len // 2
            first_half = value[:half_len]
            second_half = str(int(value[half_len:]))
            data[i] = first_half
            to_insert.append((i + 1, second_half))
    for inserted_idx, (idx, value) in enumerate(to_insert):
        data.insert(inserted_idx + idx, value)

    return data


@lru_cache(maxsize=None)
def count_stones(stone: str, blinks_left: int) -> int:
    if blinks_left == 0:
        return 1

    if stone == "0":
        return count_stones("1", blinks_left - 1)

    stone_len = len(stone)

    if stone_len % 2:
        return count_stones(str(int(stone) * 2024), blinks_left - 1)

    half_len = stone_len // 2
    first_half = stone[:half_len]
    second_half = str(int(stone[half_len:]))
    return count_stones(first_half, blinks_left - 1) + count_stones(
        second_half, blinks_left - 1
    )


def blink(data: list[str], times: int) -> int:
    all_stones = 0
    for stone in data:
        ret_val = count_stones(stone, times)
        print(f"stone {stone} has {ret_val} stones")
        all_stones += ret_val
    return all_stones


if __name__ == "__main__":
    data = read_data("day11\\input_short.txt")
    print(data)
    result = blink(data, 5)
    # print(result)
    print(f"after 75 blinks, there are {result} stones")
