import os


def new_file(path: str, name: str):
    new_file_path = f"{path}/{name}"
    with open(new_file_path, "w") as new_file:
        pass


# create folder for new day
def new_day():
    current_dir = os.getcwd()
    list_dir = os.listdir(current_dir)
    done_days = [int(d.strip("day")) for d in list_dir if d.startswith("day")]
    done_days.sort()
    new_day = done_days[-1] + 1

    new_dir = f"{current_dir}/day{new_day}"
    os.mkdir(new_dir)

    new_file(new_dir, "input.txt")
    new_file(new_dir, "input_short.txt")
    new_file(new_dir, "readme.md")
    new_file(new_dir, f"dec{new_day}.py")


if __name__ == "__main__":
    new_day()
