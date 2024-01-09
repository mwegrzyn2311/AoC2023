from utils.file_loader import load
from common import hash_str
import re


def main():
    solution(load('15.txt'))


remove_pattern = re.compile('(?P<label>\w+)-')
add_pattern = re.compile('(?P<label>\w+)=(?P<foc_len>\d+)')


def solution(lines: list[str]):
    boxes: dict[int, list[tuple[str, int]]] = {}
    for step in lines[0].split(","):
        remove_match: re.Match = remove_pattern.match(step)
        if remove_match is not None:
            label: str = remove_match.group('label')
            label_hash: int = hash_str(label)
            if label_hash in boxes:
                boxes[label_hash] = [lens for lens in boxes[label_hash] if lens[0] != label]
        else:
            add_match: re.Match = add_pattern.match(step)
            label: str = add_match.group('label')
            foc_len: int = int(add_match.group('foc_len'))
            label_hash: int = hash_str(label)
            new_lens: tuple[str, int] = (label, foc_len)
            if label_hash not in boxes:
                boxes[label_hash] = [new_lens]
            else:
                if label in [lens[0] for lens in boxes[label_hash]]:
                    boxes[label_hash] = [(lens if lens[0] != label else new_lens) for lens in boxes[label_hash]]
                else:
                    boxes[label_hash].append(new_lens)
    print(sum([sum([(box_no + 1) * (i + 1) * (box[i][1]) for i in range(len(box))]) for box_no, box in boxes.items()]))




if __name__ == '__main__':
    main()
