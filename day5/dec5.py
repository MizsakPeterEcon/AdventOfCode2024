def read_data(data_file):
    with open(data_file, "r") as file:
        loaded_data = file.readlines()
    return loaded_data


def split_data(data: list[str]):
    rule = True
    rules: dict[int, list[int]] = {}
    pages: list[list[int]] = []
    for line in data:
        line = line.strip()
        if line == "":
            rule = False
            continue

        if rule:
            p1, p2 = line.split("|")

            rules.setdefault(int(p1), [])
            rules[int(p1)].append(int(p2))

        else:
            pages.append([int(p) for p in line.split(",")])
    return rules, pages


def check_correct(rules, pages):
    correct_pages: list[list[int]] = []
    corrected_pages: list[list[int]] = []
    for page_list in pages:
        org_valid, _, _ = check_rule(page_list, rules)
        if org_valid:
            correct_pages.append(page_list)
            continue
        new_valid = make_valid(page_list, rules)
        if new_valid:
            corrected_pages.append(page_list)

    return correct_pages, corrected_pages


def check_rule(page_list: list[int], rules: dict) -> tuple[bool, int, int]:
    for page_idx, page in enumerate(page_list):
        if page not in rules:
            continue
        should_follow_pages = rules[page]
        for follow_page in should_follow_pages:
            try:
                follow_page_idx = page_list.index(follow_page)
                if follow_page_idx < page_idx:
                    return False, follow_page_idx, page_idx
            except ValueError:
                continue
    return True, -1, -1


def make_valid(page_list: list[int], rules: dict) -> bool:
    valid = False
    counter = 0
    max_counter = len(page_list) * 5
    while not valid:
        counter += 1
        valid, follow_page_idx, page_idx = check_rule(page_list, rules)
        if not valid:
            popped = page_list.pop(page_idx)
            page_list.insert(follow_page_idx, popped)
        if counter > max_counter:
            print("Max counter reached, could not correct...")
            break
    return valid


def sum_mid_values(correct_pages):
    sum_of_mids = 0
    for page_list in correct_pages:
        sum_of_mids += page_list[int((len(page_list) - 1) / 2)]
    return sum_of_mids


if __name__ == "__main__":
    data = read_data("input.txt")
    rules, pages = split_data(data)
    correct_pages, corrected_pages = check_correct(rules, pages)
    sum_of_mids = sum_mid_values(correct_pages)
    print(f"The sum of mid values: {sum_of_mids}")
    print(f"Corrected pages: {corrected_pages}")
    sum_of_corrected_mids = sum_mid_values(corrected_pages)
    print(f"The sum of mid values after correction: {sum_of_corrected_mids}")
