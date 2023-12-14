from utils.file_loader import load


def main():
    solution(load('14.txt'))


def solution(lines: list[str]):
    res: int = 0
    for x in range(len(lines[0]) - 1):
        last_stop: int = 0
        for y in range(len(lines)):
            if lines[y][x] == '#':
                last_stop = y + 1
            elif lines[y][x] == 'O':
                res += (len(lines) - last_stop)
                last_stop += 1
    print(res)

main()
