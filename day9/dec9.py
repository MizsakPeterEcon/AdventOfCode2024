from copy import deepcopy
from dataclasses import dataclass


@dataclass
class File:
    id: int
    size: int
    tried_to_move: bool = False

    def __repr__(self):
        return "".join(f"({self.id})" for _ in range(self.size))

    def calculate_checksum(self, start_idx: int):
        return sum(self.id * (i + start_idx) for i in range(self.size))


@dataclass
class FreeSpace:
    size: int

    def __repr__(self):
        return "".join("." for _ in range(self.size))

    def calculate_checksum(self, start_idx: int):
        return 0


def read_data(filename):
    with open(filename, "r") as file:
        return file.read().strip()


def create_disk_map(data: str):
    disk_map: list[File | FreeSpace] = []
    data_length = len(data)
    for idx in range(int((data_length + 1) / 2)):
        disk_map.append(File(idx, int(data[2 * idx])))
        if 2 * idx + 1 < data_length:
            disk_map.append(FreeSpace(int(data[2 * idx + 1])))
        else:
            disk_map.append(FreeSpace(0))
    return disk_map


def compact_disk_map(disk_map: list[File | FreeSpace]):
    disk_map = deepcopy(disk_map)
    next_free_space_idx = 1
    back_idx = 2
    while True:
        data_to_move = disk_map[-back_idx]
        free_space = disk_map[next_free_space_idx]
        assert isinstance(data_to_move, File)
        assert isinstance(free_space, FreeSpace)
        if free_space.size > data_to_move.size:
            disk_map.insert(next_free_space_idx, data_to_move)
            disk_map[-back_idx + 1].size += data_to_move.size
            free_space.size -= data_to_move.size
            disk_map.pop(-back_idx)
            back_idx += 1
            next_free_space_idx += 1
        elif free_space.size == data_to_move.size:
            disk_map[next_free_space_idx] = data_to_move
            disk_map[-back_idx] = free_space
            back_idx += 2
            next_free_space_idx += 2
        else:
            disk_map[next_free_space_idx] = File(data_to_move.id, free_space.size)
            disk_map[-back_idx + 1].size += free_space.size
            disk_map[-back_idx].size -= free_space.size
            next_free_space_idx += 2

        if next_free_space_idx > len(disk_map) - back_idx:
            break
    return disk_map


def compact_disk_map_without_fragmentation(disk_map: list[File | FreeSpace]):
    new_disk_map = deepcopy(disk_map)
    back_idx = 2
    while True:

        data_to_move = new_disk_map[-back_idx]
        if not isinstance(data_to_move, File) or data_to_move.tried_to_move:
            back_idx += 1
            continue
        free_space_idx = 0
        while True:
            data_to_move.tried_to_move = True
            next_free_space = new_disk_map[free_space_idx]
            if not isinstance(next_free_space, FreeSpace):
                free_space_idx += 1
                continue

            if free_space_idx > len(new_disk_map) - back_idx:
                back_idx += 1
                break

            if next_free_space.size > data_to_move.size:
                new_disk_map.insert(free_space_idx, data_to_move)
                new_disk_map[-back_idx] = FreeSpace(data_to_move.size)
                next_free_space.size -= data_to_move.size
                back_idx += 1
                break
            elif next_free_space.size == data_to_move.size:
                new_disk_map[free_space_idx] = data_to_move
                new_disk_map[-back_idx] = next_free_space
                back_idx += 1
                break

            free_space_idx += 1
        if len(new_disk_map) <= back_idx:
            break
    return new_disk_map


def calculate_checksum(disk_map: list[File | FreeSpace]) -> int:
    idx = 0
    checksum = 0
    for item in disk_map:
        checksum += item.calculate_checksum(idx)
        idx += item.size
    return checksum


if __name__ == "__main__":
    data = read_data("day9\\input.txt")
    print(data)

    disk_map = create_disk_map(data)
    print(disk_map)

    new_disk_map = compact_disk_map(disk_map)
    print(new_disk_map)

    checksum = calculate_checksum(new_disk_map)
    print(f"Checksum: {checksum}")

    defragmented_compact_disk_map = compact_disk_map_without_fragmentation(disk_map)
    print(defragmented_compact_disk_map)
    checksum = calculate_checksum(defragmented_compact_disk_map)
    print(f"Checksum: {checksum}")
