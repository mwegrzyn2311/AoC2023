import os


def load(filename: str) -> list[str]:
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    return open(os.path.join(__location__, f'../resources/{filename}'), 'r').readlines()