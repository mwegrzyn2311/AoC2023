from utils.file_loader import load
from utils.common import Vector2, NEIGH_DIRS
from functools import lru_cache


def main():
    solution(load('21.txt'))


def solution(lines: list[str]):
    @lru_cache(999999)
    def reachable_steps(curr_pos: Vector2, remaining_steps: int) -> set[Vector2]:
        if not curr_pos.is_in_map(len(lines[0]) - 1, len(lines)) or lines[curr_pos.y][curr_pos.x] == '#':
            return set()

        if remaining_steps == 0:
            return {curr_pos}

        ret: set[Vector2] = set()
        for neigh_dir in NEIGH_DIRS:
            ret = ret.union(reachable_steps(curr_pos + neigh_dir, remaining_steps - 1))
        return ret

    print(len(reachable_steps(find_start(lines), 64)))


def find_start(lines: list[str]) -> Vector2:
    for y in range(len(lines)):
        for x in range(len(lines[0]) - 1):
            if lines[y][x] == 'S':
                return Vector2(x, y)
    print("ERR: S not found")
    return Vector2(-1, -1)


if __name__ == '__main__':
    main()
