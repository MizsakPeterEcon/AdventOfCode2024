def read_data(data_file: str) -> list[str]:
    with open(data_file, "r") as file:
        _loaded_data = file.read()
    return _loaded_data.strip().split(" ")


def apply_rules(data: list[str]) -> list[str]:
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


def blink(data: list[str], times: int) -> list[str]:
    for i in range(times):
        data = apply_rules(data)
        print(f"blink {i + 1} done")
    return data


if __name__ == "__main__":
    data = read_data("day11\\input.txt")
    print(data)
    result = blink(data, 25)
    print(result)
    print(f"after 25 blinks, there are {len(result)} stones")
