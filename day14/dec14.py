import re
from dataclasses import dataclass

INPUT_PATTERN = re.compile(r"p=(\d+),(\d+) v=([^,]+),([^,]+)")


@dataclass
class Robot:
    x: int
    y: int
    vx: int
    vy: int


class Board:
    def __init__(self, size_x: int, size_y: int):
        self.size_x = size_x
        self.size_y = size_y
        self.robots: list[Robot] = []

    def add_robot(self, robot: Robot):
        self.robots.append(robot)

    def move_robots(self, times: int = 1):
        for _ in range(times):
            for robot in self.robots:
                robot.x += robot.vx
                robot.y += robot.vy
                if robot.x < 0:
                    robot.x = self.size_x + robot.x
                if robot.y < 0:
                    robot.y = self.size_y + robot.y
                if robot.x >= self.size_x:
                    robot.x = robot.x - self.size_x
                if robot.y >= self.size_y:
                    robot.y = robot.y - self.size_y
            # print("---------------------------")
            # print(f"Moved robots {_ + 1} times")
            # print("---------------------------")
            # if _ > 100:
            #     self.draw_map()
            #     time.sleep(0.2)

    def count_robots_in_quadrants(self) -> list[int]:
        quadrants = [0, 0, 0, 0]
        print(self.size_x, self.size_y)
        print(self.size_x // 2, self.size_y // 2)
        for robot in self.robots:
            if robot.x < self.size_x // 2 and robot.y < self.size_y // 2:
                quadrants[0] += 1
            elif robot.x > self.size_x // 2 and robot.y < self.size_y // 2:
                quadrants[1] += 1
            elif robot.x < self.size_x // 2 and robot.y > self.size_y // 2:
                quadrants[2] += 1
            elif robot.x > self.size_x // 2 and robot.y > self.size_y // 2:
                quadrants[3] += 1
        return quadrants

    def draw_map(self):
        possible = False
        map_ = [["." for _ in range(self.size_x)] for _ in range(self.size_y)]
        for robot in self.robots:
            map_[robot.y][robot.x] = "#"
        for y in range(self.size_y):
            if "#########" in "".join(map_[y]):
                possible = True
        return possible, map_


def read_data(data_file: str) -> list[str]:
    with open(data_file, "r") as file:
        _loaded_data = file.readlines()
    return [line.strip() for line in _loaded_data]


def multiply_list(my_list):
    result = 1
    for x in my_list:
        result = result * x
    return result


if __name__ == "__main__":
    data = read_data("day14/input.txt")
    board = Board(101, 103)
    # board = Board(11, 7)
    for line in data:
        input_match = INPUT_PATTERN.match(line)
        if not input_match:
            raise ValueError(f"Invalid input: {line}")
        x, y, vx, vy = input_match.groups()
        board.add_robot(Robot(int(x), int(y), int(vx), int(vy)))

    board.move_robots(100)
    quadrants = board.count_robots_in_quadrants()
    print(f"Safety factor is: {multiply_list(quadrants)}")

    for move in range(10001):
        if move % 100 == 0:
            print(f"Move: {move+101}")
        board.move_robots()
        possible, map_ = board.draw_map()
        if possible:
            print(f"Possible after {move+101} moves")
            for line in map_:
                print("".join(line))
