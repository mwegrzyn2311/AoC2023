import os


def main():
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    file1 = open(os.path.join(__location__, '../resources/01.txt'), 'r')
    solution(file1.readlines())


digits: dict[str, int] = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9
}

reversed_digits = {digit[::-1]: digits[digit] for digit in digits}


def solution(lines: list[str]):
    print(sum([find_digit(line, digits) * 10 + find_digit(line[::-1], reversed_digits) for line in lines]))


def find_digit(line: str, digits_dict: dict[str, int]) -> int:
    for i in range(len(line)):
        if line[i].isdigit():
            return int(line[i])
        else:
            for digit in digits_dict:
                match = True
                for j in range(len(digit)):
                    if i + j >= len(line) or digit[j] != line[i + j]:
                        match = False
                        break
                if match:
                    return digits_dict[digit]


main()
