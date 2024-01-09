from utils.file_loader import load
from utils.common import Vector2
from common import Hailstorm2D, parse_hailstorms_p1


def main():
    solution(load('24.txt'))


def solution(lines: list[str]):
    hailstorms: list[Hailstorm2D] = parse_hailstorms_p1(lines)
    coord_range: tuple[int, int] = (200000000000000, 400000000000000)
    print(len([1 for idx, h0 in enumerate(hailstorms) for h1 in hailstorms[idx + 1:] if
               intersect_inside(h0, h1, coord_range)]))


def is_parallel(vel0: Vector2, vel1: Vector2) -> bool:
    return vel0.x / vel0.y == vel1.x / vel1.y


# x = (x1 + a1 * s)
# y = (y1 + b1 * s)
def intersection_2(h1: Hailstorm2D, time: float) -> Vector2:
    x: float = h1.pos.x + h1.vel.x * time
    y: float = h1.pos.y + h1.vel.y * time
    return Vector2(x, y)


# t = (x0b1 - x1b1 - y0a1 + y1a1) / (a1b0 - a0b1)
# t = (a1 * (y1 - y0) - b1 * (x1 - x0)) / (a1b0 - a0b1)
def intersection_time_1(h0: Hailstorm2D, h1: Hailstorm2D) -> float:
    return (h1.vel.x * (h1.pos.y - h0.pos.y) - h1.vel.y * (h1.pos.x - h0.pos.x)) / (
                h1.vel.x * h0.vel.y - h0.vel.x * h1.vel.y)


# s = (y1a0 - y0a0 - x1b0 + x0b0) / (a1b0 - a0b1)
# s = (a0 * (y1 - y0) - b0 * (x1 - x0)) / (a1b0 - a0b1)
def intersection_time_2(h0: Hailstorm2D, h1: Hailstorm2D) -> float:
    return (h0.vel.x * (h1.pos.y - h0.pos.y) - h0.vel.y * (h1.pos.x - h0.pos.x)) / (
                h1.vel.x * h0.vel.y - h0.vel.x * h1.vel.y)


def intersect_inside(h0: Hailstorm2D, h1: Hailstorm2D, coord_range: tuple[int, int]) -> bool:
    print("------")
    if not is_parallel(h0.vel, h1.vel):
        intersect_time_1: float = intersection_time_1(h0, h1)
        intersect_time_2: float = intersection_time_2(h0, h1)
        print(intersect_time_1)
        print(intersect_time_2)
        if intersect_time_1 >= 0 and intersect_time_2 >= 0:
            intersect_coord: Vector2 = intersection_2(h1, intersect_time_2)
            if coord_range[0] <= intersect_coord.x <= coord_range[1] and coord_range[0] <= intersect_coord.y <= \
                    coord_range[1]:
                print(h0, h1)
                print(f'Inside {intersect_coord}')
                print(intersection_2(h1, intersect_time_2))
                return True
            else:
                print(f'Outside {intersect_coord}')
        else:
            print(h0, h1)
            print("Before")
            print(intersection_2(h1, intersect_time_2))
    else:
        print("Parallel")
    return False


if __name__ == '__main__':
    main()
