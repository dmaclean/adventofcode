import dataclasses
from typing import List, Optional


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

    def calc_total_size(self, threshold: int, accumulator: List[int]) -> int:
        total = sum(f.size for f in self.files) + \
                sum(d.calc_total_size(threshold, accumulator) for d in self.dirs)
        if total < threshold:
            accumulator.append(total)
        return total


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

    accumulator = []
    root.calc_total_size(100000, accumulator)
    print(sum(accumulator))
