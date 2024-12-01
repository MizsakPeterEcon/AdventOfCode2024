def read_data(data_file):
    with open(data_file, "r") as file:
        loc_data = file.readlines()

    loc_ids_1 = []
    loc_ids_2 = []
    for line in loc_data:
        loc_id1, loc_id2 = line.split()
        loc_ids_1.append(int(loc_id1))
        loc_ids_2.append(int(loc_id2))
    return loc_ids_1, loc_ids_2


def calculate_difference(loc_ids_1: list, loc_ids_2: list):
    loc_ids_1.sort()
    loc_ids_2.sort()

    diff = 0
    for loc_id1, loc_id2 in zip(loc_ids_1, loc_ids_2):
        diff += abs(loc_id1 - loc_id2)

    print(f"The diff score id: {diff}")


def calculate_similiarity(loc_ids_1: list, loc_ids_2: list):
    similarity = 0

    for loc_id1 in loc_ids_1:
        repeat = loc_ids_2.count(loc_id1)
        similarity += loc_id1 * repeat

    print(f"The similarity score is: {similarity}")


if __name__ == "__main__":
    list1, list2 = read_data("input.txt")

    calculate_difference(list1, list2)
    calculate_similiarity(list1, list2)
