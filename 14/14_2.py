from utils.file_loader import load
import copy


def main():
    solution(load('14.txt'))


def solution(lines: list[str]):
    past_states: list[list[str]] = []
    after_cycle: list[str] = [line[:-1] for line in lines]
    while after_cycle not in past_states:
        past_states.append(after_cycle)
        after_cycle = cycle(copy.deepcopy(after_cycle))
    repeat_len = len(past_states) - past_states.index(after_cycle)

    print(calculate_load(past_states[len(past_states) - repeat_len + (1000000000 - len(past_states)) % repeat_len]))


def calculate_load(lines: list[str]) -> int:
    return sum([sum([len(lines) - y for x in range(len(lines[0])) if lines[y][x] == 'O']) for y in range(len(lines))])


def cycle(lines: list[str]) -> list[str]:
    # north
    for x in range(len(lines[0])):
        last_stop: int = 0
        for y in range(len(lines)):
            if lines[y][x] == '#':
                last_stop = y + 1
            elif lines[y][x] == 'O':
                lines[y] = str_insert(lines[y], x, lines[last_stop][x])
                lines[last_stop] = str_insert(lines[last_stop], x, 'O')
                last_stop += 1
    # west
    for y in range(len(lines)):
        last_stop: int = 0
        for x in range(len(lines)):
            if lines[y][x] == '#':
                last_stop = x + 1
            elif lines[y][x] == 'O':
                if x != last_stop:
                    lines[y] = str_insert(lines[y], x, lines[y][last_stop])
                    lines[y] = str_insert(lines[y], last_stop, 'O')
                last_stop += 1
    # south
    for x in range(len(lines[0])):
        last_stop: int = len(lines) - 1
        for y in range(len(lines) - 1, -1, -1):
            if lines[y][x] == '#':
                last_stop = y - 1
            elif lines[y][x] == 'O':
                lines[y] = str_insert(lines[y], x, lines[last_stop][x])
                lines[last_stop] = str_insert(lines[last_stop], x, 'O')
                last_stop -= 1
    # west
    for y in range(len(lines)):
        last_stop: int = len(lines[0]) - 1
        for x in range(len(lines) - 1, -1, -1):
            if lines[y][x] == '#':
                last_stop = x - 1
            elif lines[y][x] == 'O':
                if x != last_stop:
                    lines[y] = str_insert(lines[y], x, lines[y][last_stop])
                    lines[y] = str_insert(lines[y], last_stop, 'O')
                last_stop -= 1
    return lines


def str_insert(original: str, i: int, char: str) -> str:
    return original[:i] + char + original[i + 1:]


main()
