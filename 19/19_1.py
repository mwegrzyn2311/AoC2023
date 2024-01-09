from utils.file_loader import load
from common1 import Workflow


def main():
    solution(load('19.txt'))


def solution(lines: list[str]):
    i: int = 0
    while lines[i] != '\n':
        Workflow(lines[i])
        i += 1

    i += 1

    parts: list[dict[str, int]] = []
    while i < len(lines) and lines[i] and lines[i] != '\n':
        parts.append({category.split('=')[0]: int(category.split('=')[1]) for category in lines[i].strip('{}\n').split(',')})
        i += 1

    print(sum([sum(part.values()) for part in parts if Workflow.workflows['in'].apply(part)]))


if __name__ == '__main__':
    main()
