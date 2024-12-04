def is_safe(report):
    """Check if the report is safe."""
    increasing = all(report[i] < report[i+1] and 1 <= report[i+1] - report[i] <= 3 for i in range(len(report) - 1))
    decreasing = all(report[i] > report[i+1] and 1 <= report[i] - report[i+1] <= 3 for i in range(len(report) - 1))
    return increasing or decreasing

def is_safe_with_dampener(report):
    """Check if the report is safe with one level removed."""
    for i in range(len(report)):
        modified_report = report[:i] + report[i+1:]
        if is_safe(modified_report):
            return True
    return False

def count_safe_reports(reports):
    """Count the number of safe reports."""
    return sum(1 for report in reports if is_safe(report))

def count_safe_reports_with_dampener(reports):
    """Count the number of safe reports with the dampener."""
    return sum(1 for report in reports if is_safe(report) or is_safe_with_dampener(report))

def parse_input(file_path):
    """Parse the input file into a list of reports."""
    with open(file_path, 'r') as file:
        return [list(map(int, line.split())) for line in file]

if __name__ == "__main__":
    reports = parse_input("input.txt")
    print("Part 1: Safe reports count:", count_safe_reports(reports))
    print("Part 2: Safe reports count with dampener:", count_safe_reports_with_dampener(reports))
