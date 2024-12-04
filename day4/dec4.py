def read_data(data_file):
    with open(data_file, "r") as file:
        loaded_data = file.readlines()
    return loaded_data


def find_in_text(text_data: list[str]) -> int:
    match_count = 0
    for line in text_data:
        match_count += line.count("XMAS")
        match_count += line.count("SAMX")
    return match_count


def transpose_data(text_data: list[str]) -> list[str]:
    new_data = []
    for c in range(len(text_data[0].strip())):
        new_data.append("".join([row[c] for row in text_data]))
    return new_data


def get_diagonals(text_data: list[str]) -> tuple[list[str], list[str]]:
    rows = len(text_data)
    cols = len(text_data[0].strip())

    new_data_1 = []
    for line_idx in range(1, (rows + cols)):
        start_col = max(0, line_idx - rows)
        line_length = min(line_idx, (cols - start_col), rows)
        new_data_1.append(
            "".join(
                [
                    text_data[min(rows, line_idx) - j - 1][start_col + j]
                    for j in range(0, line_length)
                ]
            )
        )

    new_data_2 = []
    for line_idx in range(1, (rows + cols)):
        start_row = max(0, line_idx - cols)
        line_length = min(line_idx, (rows - start_row), cols)
        new_data_2.append(
            "".join(
                [
                    text_data[start_row + j][cols - (min(cols, line_idx) - j)]
                    for j in range(0, line_length)
                ]
            )
        )

    return new_data_1, new_data_2


def find_x_mas(text_data: list[str]) -> int:
    rows = len(text_data)
    cols = len(text_data[0].strip())
    x_max_count = 0
    for r in range(rows - 2):
        for c in range(cols - 2):
            segment = [l[c : c + 3] for l in text_data[r : r + 3]]
            if ("".join([segment[i][i] for i in range(3)]) in ["MAS", "SAM"]) and (
                "".join([segment[i][2 - i] for i in range(3)]) in ["MAS", "SAM"]
            ):
                x_max_count += 1
    return x_max_count


if __name__ == "__main__":
    data = read_data("input.txt")

    horizontal_matches = find_in_text(data)
    print(f"{horizontal_matches=}")

    transp_data = transpose_data(data)
    vertical_matches = find_in_text(transp_data)
    print(f"{vertical_matches=}")

    diag_1_data, diag_2_data = get_diagonals(data)
    diag_1_matches = find_in_text(diag_1_data)
    diag_2_matches = find_in_text(diag_2_data)

    print(f"{diag_1_matches=}")
    print(f"{diag_2_matches=}")
    print(
        f"all matches: {horizontal_matches+vertical_matches+diag_1_matches+diag_2_matches}"
    )
    x_mas_matches = find_x_mas(data)
    print(f"all x_mas_matches: {x_mas_matches}")

    # print(*diag_1_data, sep="\n")
    # print(*diag_2_data, sep="\n")
