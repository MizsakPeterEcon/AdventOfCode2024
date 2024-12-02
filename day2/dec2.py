def read_data(data_file):
    with open(data_file, "r") as file:
        loaded_reports = file.readlines()

    reports = []
    for report in loaded_reports:
        reports.append([int(x) for x in report.split()])

    return reports


def get_diffs(levels: list[int]) -> list[int]:
    diffs = [j - i for i, j in zip(levels[:-1], levels[1:])]
    return diffs


def check_safe(diff: list[int]) -> bool:
    if all(0 < i <= 3 for i in diff):
        return True
    if all(-3 <= i < 0 for i in diff):
        return True

    return False


def make_safe(levels: list[int]) -> bool:
    for i in range(len(levels)):
        new_levels = levels.copy()
        new_levels.pop(i)
        diff = get_diffs(new_levels)
        safe = check_safe(diff)
        if safe:
            return True
    return False


def count_safe(reports):
    already_safe_count = 0
    made_safe_count = 0
    for report in reports:
        diff = get_diffs(report)
        if check_safe(diff):
            already_safe_count += 1
            print(f"report {report} is safe already")
            continue
        if make_safe(report):
            made_safe_count += 1
            print(f"report {report} is made safe")
    return already_safe_count, made_safe_count


if __name__ == "__main__":

    reports = read_data("input.txt")
    already_safe, made_safe = count_safe(reports)
    print(
        f"Number of safe reports: {already_safe + made_safe}, (originally: {already_safe})"
    )
