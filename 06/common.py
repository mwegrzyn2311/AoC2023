from math import floor, ceil, sqrt


def roots_diff(t: int, s: int) -> int:
    delta: float = sqrt(t * t - 4 * s)
    return x2(t, delta) - x1(t, delta) + 1


def x1(t: int, delta: float) -> int:
    x: float = (t - delta) / 2.0
    return int(x + 1) if x.is_integer() else ceil(x)


def x2(t: int, delta: float) -> int:
    x: float = (t + delta) / 2
    return int(x - 1) if x.is_integer() else floor(x)
