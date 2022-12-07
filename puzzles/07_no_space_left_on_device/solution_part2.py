import dataclasses
from typing import List, Optional

TOTAL_DISK_SPACE = 70_000_000

TARGET_FREE_SPACE = 30_000_000


@dataclasses.dataclass
class File:
    size: int
    name: str


@dataclasses.dataclass
class Directory:
    name: str
    parent: Optional["Directory"]
    dirs: List["Directory"]
    files: List[File]

    def find_child_dir(self, name: str) -> Optional["Directory"]:
        for d in self.dirs:
            if d.name == name:
                return d
        return None

    def add_child_dir(self, dir: "Directory") -> None:
        self.dirs.append(dir)

    def add_file(self, file: File) -> None:
        self.files.append(file)

    def calc_total_size(self) -> int:
        return sum(f.size for f in self.files) + \
            sum(d.calc_total_size() for d in self.dirs)

    def find_dir_with_min_size(self, needed_free_space: int) -> int:
        """
        Recursive method to determine the smallest directory over a certain threshold
        :param needed_free_space: The amount of free space needed (threshold)
        """
        min_from_children = None
        for d in self.dirs:
            val = d.find_dir_with_min_size(needed_free_space)
            if val >= needed_free_space and (min_from_children is None or min_from_children > val):
                min_from_children = val
        if min_from_children is not None and min_from_children >= needed_free_space:
            return min_from_children
        return self.calc_total_size()


root = Directory('/', None, [], [])
curr_dir = root
with open('input.txt') as f:
    for line in f.readlines():
        trimmed = line.strip()
        if trimmed == '$ cd /':
            continue
        if trimmed.startswith('$'):
            # Command
            cmd = trimmed.split(' ')
            if cmd[1] == 'cd':
                dir_name = cmd[2]
                if dir_name == '..':
                    curr_dir = curr_dir.parent
                # elif dir_name == curr_dir.name:
                #     We are already in this directory
                # continue
                else:
                    child_dir = curr_dir.find_child_dir(dir_name)
                    if not child_dir:
                        raise Exception(f'Could not find directory {dir_name} from {curr_dir.name}')
                    curr_dir = child_dir

            # I don't think we care if an `ls` command is issued as long as we are in the right directory

        elif trimmed.startswith('dir'):
            # Directory
            parts = trimmed.split(' ')
            child = Directory(parts[1], curr_dir, [], [])
            curr_dir.add_child_dir(child)
        else:
            # File
            parts = trimmed.split(' ')
            file = File(int(parts[0]), parts[1])
            curr_dir.add_file(file)

    used_space = root.calc_total_size()
    free_space = TOTAL_DISK_SPACE - used_space
    needed_free_space = TARGET_FREE_SPACE - free_space

    print(needed_free_space)
    print(root.find_dir_with_min_size(needed_free_space))
