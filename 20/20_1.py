from utils.file_loader import load
from common import parse_modules, Controller, Pulse


def main():
    solution(load('20.txt'))


def solution(lines: list[str]):
    controller: Controller = parse_modules(lines)
    controller.play_until_repeat()
    print(controller.pulses)
    print(f'{sum(controller.pulses[Pulse.LOW])} - {sum(controller.pulses[Pulse.HIGH])}')
    print(f'{sum(controller.pulses[Pulse.LOW]) * sum(controller.pulses[Pulse.HIGH])}')


if __name__ == '__main__':
    main()
