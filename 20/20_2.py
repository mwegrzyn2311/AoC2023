from math import lcm

from utils.file_loader import load
from common import parse_modules, Controller, Pulse


def main():
    solution(load('20.txt'))


def solution(lines: list[str]):
    controller: Controller = parse_modules(lines)
    controller.play_until_module_on('lz')
    print(controller.cycles)
    # lk = 4001, ft = 3851, qr = 4013, lz = 3911
    print(lcm(4001, 3851, 4013, 3911))
# 61831706063 too low

if __name__ == '__main__':
    main()
