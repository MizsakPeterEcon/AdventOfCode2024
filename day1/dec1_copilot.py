def read_input(file_path):
    """
    Reads the input file and returns two lists of integers.
    """
    with open(file_path, "r") as file:
        left_list = []
        right_list = []
        for line in file:
            left, right = map(int, line.split())
            left_list.append(left)
            right_list.append(right)
    return left_list, right_list


def calculate_total_distance(left_list, right_list):
    """
    Calculates the total distance between two lists of integers.
    """
    left_list.sort()
    right_list.sort()
    total_distance = sum(abs(l - r) for l, r in zip(left_list, right_list))
    return total_distance


def calculate_similarity_score(left_list, right_list):
    """
    Calculates the similarity score between two lists of integers.
    """
    from collections import Counter

    right_counter = Counter(right_list)
    similarity_score = sum(l * right_counter[l] for l in left_list)
    return similarity_score


if __name__ == "__main__":
    left_list, right_list = read_input("input.txt")

    # Part One
    total_distance = calculate_total_distance(left_list, right_list)
    print(f"Total Distance: {total_distance}")

    # Part Two
    similarity_score = calculate_similarity_score(left_list, right_list)
    print(f"Similarity Score: {similarity_score}")
