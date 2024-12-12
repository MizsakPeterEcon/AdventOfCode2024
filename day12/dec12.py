from dataclasses import dataclass

# row, column
DIRS = {"right": (0, 1), "down": (1, 0), "left": (0, -1), "up": (-1, 0)}


@dataclass
class FenceSection:
    start: int
    end: int
    direction: str
    coordinate: int

    def check_of_connected(
        self, direction: str, coordinate: int, position: int
    ) -> bool:
        if not self.direction == direction:
            return False
        if not self.coordinate == coordinate:
            return False
        if self.start <= position <= self.end:
            return False
        if position == self.start - 1:
            return True
        if position == self.end + 1:
            return True

        return False

    def add_section(self, position: int) -> None:
        if position == self.start - 1:
            self.start = position
            return
        if position == self.end + 1:
            self.end = position
            return
        raise ValueError(f"Invalid position {self}, {position}")


@dataclass
class GardenRegion:
    coordinates: list[tuple[int, int]]
    plant_type: str

    def __str__(self) -> str:
        max_row = max(self.coordinates, key=lambda x: x[0])[0]
        max_col = max(self.coordinates, key=lambda x: x[1])[1]
        min_row = min(self.coordinates, key=lambda x: x[0])[0]
        min_col = min(self.coordinates, key=lambda x: x[1])[1]
        grid = [
            ["." for _ in range(max_col - min_col + 1)]
            for _ in range(max_row - min_row + 1)
        ]
        for coord in self.coordinates:
            grid[coord[0] - min_row][coord[1] - min_col] = self.plant_type
        return "\n" + "\n".join("".join(row) for row in grid) + "\n"

    def sort_coordinates(self) -> None:
        self.coordinates.sort(key=lambda x: (x[0], x[1]))

    def calculate_area(self) -> int:
        return len(self.coordinates)

    def calculate_perimeter(self) -> int:
        perimeter = 0
        for coord in self.coordinates:
            for dir_ in DIRS.values():
                new_coord = (coord[0] + dir_[0], coord[1] + dir_[1])
                if new_coord not in self.coordinates:
                    perimeter += 1
        return perimeter

    def calculate_perimeter_sections(self) -> int:
        sides: list[FenceSection] = []
        for coord in self.coordinates:
            for dir_name, dir_ in DIRS.items():
                new_coord = (coord[0] + dir_[0], coord[1] + dir_[1])
                if new_coord not in self.coordinates:
                    if dir_name == "right":
                        position = coord[0]
                        coordinate = coord[1] + 1
                    elif dir_name == "down":
                        position = coord[1]
                        coordinate = coord[0] + 1
                    elif dir_name == "left":
                        position = coord[0]
                        coordinate = coord[1]
                    elif dir_name == "up":
                        position = coord[1]
                        coordinate = coord[0]
                    for fence in sides:
                        if fence.check_of_connected(dir_name, coordinate, position):
                            fence.add_section(position)
                            break
                    else:
                        sides.append(
                            FenceSection(position, position, dir_name, coordinate)
                        )
        return len(sides)


def read_data(data_file: str) -> list[list[str]]:
    with open(data_file, "r") as file:
        _loaded_data = file.readlines()
    return [list(line.strip()) for line in _loaded_data]


def find_regions(data: list[list[str]]) -> list[GardenRegion]:
    garden_size = len(data), len(data[0])
    covered_coords = set()
    garden_regions = []

    for r in range(garden_size[0]):
        for c in range(garden_size[1]):
            coord = (r, c)
            if coord in covered_coords:
                continue
            plant_type = data[r][c]
            region = GardenRegion([coord], plant_type)
            covered_coords.add(coord)
            iterate_neighbours(coord, region, covered_coords, data, garden_size)
            garden_regions.append(region)
    return garden_regions


def iterate_neighbours(
    coord: tuple[int, int],
    region: GardenRegion,
    covered_coords: set[tuple[int, int]],
    data: list[list[str]],
    garden_size: tuple[int, int],
):
    for dir_ in DIRS.values():
        new_coord = (coord[0] + dir_[0], coord[1] + dir_[1])
        if new_coord in covered_coords:
            continue
        if (
            new_coord[0] >= 0
            and new_coord[0] < garden_size[0]
            and new_coord[1] >= 0
            and new_coord[1] < garden_size[1]
        ):
            if data[new_coord[0]][new_coord[1]] == region.plant_type:
                region.coordinates.append(new_coord)
                covered_coords.add(new_coord)
                iterate_neighbours(new_coord, region, covered_coords, data, garden_size)


if __name__ == "__main__":
    data = read_data("day12\\input.txt")
    # print(data)
    regions = find_regions(data)
    # print(regions)

    # Part 1
    cost = sum(
        region.calculate_area() * region.calculate_perimeter() for region in regions
    )
    print(f"Total cost: {cost}")
    # Part 2
    for region in regions:
        region.sort_coordinates()
        # print(region)
    cost_with_discount = sum(
        region.calculate_area() * region.calculate_perimeter() for region in regions
    )
    print(f"Total cost with discount: {cost_with_discount}")
