def count_xmas(grid):
    def search_word(x, y, dx, dy):
        for i in range(4):
            if not (0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y] == "XMAS"[i]):
                return 0
            x += dx
            y += dy
        return 1

    directions = [(1, 0), (0, 1), (1, 1), (-1, 1), (1, -1), (0, -1), (-1, 0), (-1, -1)]
    count = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            for dx, dy in directions:
                count += search_word(i, j, dx, dy)
    return count

def count_x_mas(grid):
    def search_x_mas(x, y):
        patterns = [
            [(0, 0), (1, 1), (2, 2)],  # Diagonal \
            [(0, 2), (1, 1), (2, 0)],  # Diagonal /
            [(0, 0), (1, 0), (2, 0)],  # Vertical
            [(0, 2), (1, 2), (2, 2)],  # Vertical
            [(0, 0), (0, 1), (0, 2)],  # Horizontal
            [(2, 0), (2, 1), (2, 2)]   # Horizontal
        ]
        count = 0
        for pattern in patterns:
            if all(0 <= x + dx < len(grid) and 0 <= y + dy < len(grid[0]) and grid[x + dx][y + dy] == "MAS"[i] for i, (dx, dy) in enumerate(pattern)):
                count += 1
        return count

    count = 0
    for i in range(len(grid) - 2):
        for j in range(len(grid[0]) - 2):
            if grid[i + 1][j + 1] == 'M':
                count += search_x_mas(i, j)
    return count

def read_input(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

if __name__ == "__main__":
    grid = read_input("input.txt")
    print("Count of XMAS:", count_xmas(grid))
    print("Count of X-MAS:", count_x_mas(grid))
