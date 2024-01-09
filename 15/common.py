from functools import reduce


def hash_str(string: str) -> int:
    return reduce(lambda res, char: ((res + ord(char)) * 17) % 256, string, 0)
