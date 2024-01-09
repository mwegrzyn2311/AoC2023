from utils.file_loader import load
from utils.common import Vector2, vec_from_str, NEIGH_DIRS, UP, DOWN, LEFT, RIGHT
from sys import setrecursionlimit


def main():
    solution(load('18.txt'))


NUM_TO_VEC: dict[int, Vector2] = {
    0: RIGHT,
    1: DOWN,
    2: LEFT,
    3: UP
}


def solution(lines: list[str]):
    curr_pos: Vector2 = Vector2(0, 0)
    vertices: list[Vector2] = []
    exterior_surf: int = 0
    for line in lines:
        hexadec: str = line.split()[2][2:-1]
        dig_len: int = int(hexadec[0:-1], 16)
        dig_dir: Vector2 = NUM_TO_VEC[int(hexadec[-1])]
        exterior_surf += dig_len
        curr_pos = curr_pos + dig_dir * dig_len
        vertices.append(curr_pos)
    print(int(exterior_surf/2) + 1 + calc_surf(vertices))


def calc_surf(vertices: list[Vector2]) -> int:
    return int(abs(sum([(vertices[i - 1].x + vertices[i].x) * (- vertices[i - 1].y + vertices[i].y) for i in range(len(vertices))]) / 2))

if __name__ == '__main__':
    main()
