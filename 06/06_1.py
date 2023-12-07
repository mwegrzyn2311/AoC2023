import re
from utils.file_loader import load
from functools import reduce
from common import roots_diff


def main():
    solution(load('06.txt'))


times_pattern = 'Time:\s+(?P<times>.*)'
dist_pattern = 'Distance:\s+(?P<dist>.*)'


def solution(lines: list[str]):
    times: list[int] = [int(time) for time in re.search(times_pattern, lines[0]).group('times').split()]
    dists: list[int] = [int(dist) for dist in re.search(dist_pattern, lines[1]).group('dist').split()]
    print(reduce((lambda x, y: x * y), [roots_diff(times[i], dists[i]) + 1 for i in range(len(times))]))

# s = (t) * (T - t)
# Tt - t^2 > S
# t^2 - tT + S < 0
# Delta = T^2 - 4S
# x1 = (T - sqrt(T^2 - 4S)) / 2
# x2 = (T + sqrt(T^2 - 4S)) / 2

main()
