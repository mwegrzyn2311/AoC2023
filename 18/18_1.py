from utils.file_loader import load
from utils.common import Vector2, vec_from_str, NEIGH_DIRS
from sys import setrecursionlimit


def main():
    solution(load('18.txt'))


def solution(lines: list[str]):
    # curr_pos = Vector2(0, 0)
    # lagoon: dict[Vector2, str] = {curr_pos: ''}
    # for line in lines:
    #     line_parts: list[str] = line.split()
    #     dig_dir: Vector2 = vec_from_str(line_parts[0])
    #     for i in range(int(line_parts[1])):
    #         curr_pos += dig_dir
    #         lagoon[curr_pos] = line_parts[2]
    # print(len(lagoon))
    # setrecursionlimit(99999)
    # dig_interior(lagoon, Vector2(1, 1))
    #print(len(lagoon))
    curr_pos: Vector2 = Vector2(0, 0)
    vertices: list[Vector2] = []
    exterior_surf: int = 0
    for line in lines:
        line_parts: list[str] = line.split()
        dig_dir: Vector2 = vec_from_str(line_parts[0])
        dig_len = int(line_parts[1])
        exterior_surf += dig_len
        curr_pos = curr_pos + dig_dir * dig_len
        vertices.append(curr_pos)
    print(int(exterior_surf/2) + 1 + calc_surf(vertices))


def calc_surf(vertices: list[Vector2]) -> int:
    return int(sum([(vertices[i].x + vertices[i - 1].x) * (vertices[i].y - vertices[i - 1].y) for i in range(len(vertices))]) / 2)


def dig_interior(lagoon: dict[Vector2, str], curr_pos: Vector2):
    if curr_pos in lagoon:
        return
    lagoon[curr_pos] = ''
    for neigh_dir in NEIGH_DIRS:
        dig_interior(lagoon, curr_pos + neigh_dir)


if __name__ == '__main__':
    main()
