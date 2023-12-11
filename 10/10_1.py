from utils.file_loader import load
from collections.abc import Callable


def main():
    solution(load('10.txt'))


char_to_transform: dict[str, Callable[[int, int], tuple[int, int]]] = {
    "|": lambda x, y: (x, -y),
    "-": lambda x, y: (-x, y),
    "L": lambda x, y: (-y, -x),
    "7": lambda x, y: (-y, -x),
    "J": lambda x, y: (y, x),
    "F": lambda x, y: (y, x)
}


def solution(lines: list[str]):
    start: tuple[int, int] = next((line.index("S"), j) for j, line in enumerate(lines) if "S" in line)
    curr_pos: tuple[int, int] = start
    next_pos: tuple[int, int] = find_next_to_start(start, lines)
    pipe_len: int = 1
    while lines[next_pos[1]][next_pos[0]] != "S":
        transform: tuple[int, int] = char_to_transform[lines[next_pos[1]][next_pos[0]]](curr_pos[0] - next_pos[0], curr_pos[1] - next_pos[1])
        curr_pos = next_pos
        next_pos = next_pos[0] + transform[0], next_pos[1] + transform[1]
        pipe_len += 1
    print(int(pipe_len / 2))


def find_next_to_start(start: tuple[int, int], lines: list[str]) -> tuple[int, int]:
    char_above: str = lines[start[1] - 1][start[0]]
    if char_above == "|" or char_above == "7" or char_above == "F":
        return start[0], start[1] - 1
    char_below: str = lines[start[1] + 1][start[0]]
    if char_below == "I" or char_below == "J" or char_below == "L":
        return start[0], start[1] + 1
    char_left: str = lines[start[1]][start[0] - 1]
    if char_left == "-" or char_left == "L" or char_left == "F":
        return start[0] - 1, start[1]
    char_right: str = lines[start[1]][start[0] + 1]
    if char_right == "-" or char_right == "J" or char_right == "7":
        return start[0] + 1, start[1]
    print("ERROR")
    return -1, -1


main()
