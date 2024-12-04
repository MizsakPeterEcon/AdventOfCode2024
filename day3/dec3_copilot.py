import re

def parse_input(file_path):
    """Read and return the content of the input file."""
    with open(file_path, 'r') as file:
        return file.read()

def extract_mul_instructions(data):
    """Extract valid mul instructions from the data."""
    pattern = re.compile(r'mul\((\d+),(\d+)\)')
    return [(int(x), int(y)) for x, y in pattern.findall(data)]

def calculate_sum(data, consider_conditions=False):
    """Calculate the sum of mul instructions, optionally considering do() and don't() conditions."""
    enabled = True
    total_sum = 0
    index = 0

    while index < len(data):
        if consider_conditions:
            if data[index:index+7] == "don't()":
                enabled = False
                index += 7
                continue
            elif data[index:index+4] == "do()":
                enabled = True
                index += 4
                continue

        if data[index:index+4] == "mul(":
            match = re.match(r'mul\((\d+),(\d+)\)', data[index:])
            if match:
                if enabled:
                    x, y = map(int, match.groups())
                    total_sum += x * y
                index += len(match.group(0))
                continue
        index += 1

    return total_sum

def main():
    """Main function to execute the program."""
    data = parse_input('input.txt')
    
    # Task 1: Calculate sum without considering conditions
    result_task1 = calculate_sum(data, consider_conditions=False)
    print(f"Task 1 result: {result_task1}")
    
    # Task 2: Calculate sum considering conditions
    result_task2 = calculate_sum(data, consider_conditions=True)
    print(f"Task 2 result: {result_task2}")

if __name__ == "__main__":
    main()
