import re
from operator import mul

MUL_PATTERN = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")


def read_data(data_file):
    with open(data_file, "r") as file:
        loaded_program = file.read()
    return loaded_program


def find_and_sum_all_multiplications(input_data):
    mul_sum = 0
    for match in MUL_PATTERN.finditer(input_data):
        mul_sum += mul(*[int(v) for v in match.groups()])
    return mul_sum


def find_do_sections(input_data: str):

    dont_sections = input_data.split("don't()")
    do_sections = [dont_sections.pop(0)]
    for dont_section in dont_sections:
        do_sections.append(dont_section.partition("do()")[2])

    active_program = "".join(do_sections)
    return active_program


if __name__ == "__main__":
    input_data = read_data("input.txt")
    sum_of_muls = find_and_sum_all_multiplications(input_data)
    print(f"Sum of all multiplications: {sum_of_muls}")

    active_data = find_do_sections(input_data)
    sum_of_active_muls = find_and_sum_all_multiplications(active_data)
    print(f"Sum of active multiplications: {sum_of_active_muls}")
