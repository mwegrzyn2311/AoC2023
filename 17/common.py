import bisect

from utils.common import Vector2, NEIGH_DIRS


def find_shortest_path_v3(lines: list[str]) -> int:
    shortest_paths: dict[tuple[Vector2, Vector2, int], int] = {(Vector2(0, 0), Vector2(-1, -1), 0): 0}
    visited: dict[tuple[Vector2, Vector2, int], bool] = {}
    for y in range(len(lines)):
        for x in range(len(lines[0])):
            for i in range(1, 4):
                for neigh in NEIGH_DIRS:
                    visited[(Vector2(x, y), neigh, i)] = False
    visited[(Vector2(0, 0), Vector2(-1, -1), 0)] = False

    goal: Vector2 = Vector2(len(lines[0]) - 1, len(lines) - 1)
    node_queue: list[tuple[int, tuple[Vector2, Vector2, int]]] = [(0, (Vector2(0, 0), Vector2(-1, -1), 0))]
    while len(node_queue) > 0:
        dist, curr_node = node_queue.pop(0)
        if curr_node[0] == goal:
            break
        if visited[curr_node]:
            continue
        visited[curr_node] = True
        if len(shortest_paths.keys()) % 1000 == 0:
            print(len(shortest_paths.keys()))
        for neigh_dir in NEIGH_DIRS:
            dest: Vector2 = curr_node[0] + neigh_dir
            if neigh_dir.is_opposite_vector(curr_node[1]) or (
                    curr_node[1] == neigh_dir and curr_node[2] == 3) or not dest.is_in_map(len(lines[0]), len(lines)):
                continue
            new_dist: int = dist + int(lines[dest.y][dest.x])
            next_node: tuple[Vector2, Vector2, int] = (dest, neigh_dir, curr_node[2] + 1 if curr_node[1] == neigh_dir else 1)
            if next_node not in shortest_paths:
                shortest_paths[next_node] = new_dist
            else:
                shortest_paths[next_node] = min(shortest_paths[next_node], new_dist)
            bisect.insort(node_queue, (new_dist, next_node))
    return min([val for node, val in shortest_paths.items() if node[0] == goal])


def find_shortest_path_p2(lines: list[str]) -> int:
    shortest_paths: dict[tuple[Vector2, Vector2, int], int] = {(Vector2(0, 0), Vector2(-1, -1), 0): 0}
    visited: dict[tuple[Vector2, Vector2, int], bool] = {}
    for y in range(len(lines)):
        for x in range(len(lines[0])):
            for i in range(4, 11):
                for neigh in NEIGH_DIRS:
                    visited[(Vector2(x, y), neigh, i)] = False
    visited[(Vector2(0, 0), Vector2(-1, -1), 0)] = False

    goal: Vector2 = Vector2(len(lines[0]) - 1, len(lines) - 1)
    node_queue: list[tuple[int, tuple[Vector2, Vector2, int]]] = [(0, (Vector2(0, 0), Vector2(-1, -1), 0))]
    while len(node_queue) > 0:
        dist, curr_node = node_queue.pop(0)
        if curr_node[0] == goal:
            break
        if visited[curr_node]:
            continue
        visited[curr_node] = True
        if len(shortest_paths.keys()) % 1000 == 0:
            print(len(shortest_paths.keys()))
        for neigh_dir in NEIGH_DIRS:
            if neigh_dir.is_opposite_vector(curr_node[1]):
                continue
            elif curr_node[1] == neigh_dir:
                if curr_node[2] == 10:
                    continue
                dest: Vector2 = curr_node[0] + neigh_dir
                if not dest.is_in_map(len(lines[0]), len(lines)):
                    continue
                new_dist: int = dist + int(lines[dest.y][dest.x])
                new_repeats: int = curr_node[2] + 1
            else:
                dest: Vector2 = curr_node[0] + neigh_dir * 4
                if not dest.is_in_map(len(lines[0]), len(lines)):
                    continue
                new_dist: int = dist
                new_repeats: int = 4
                for i in range(4):
                    new_dist += int(lines[dest.y - neigh_dir.y * i][dest.x - neigh_dir.x * i])
            next_node: tuple[Vector2, Vector2, int] = (dest, neigh_dir, new_repeats)
            if next_node not in shortest_paths:
                shortest_paths[next_node] = new_dist
            else:
                shortest_paths[next_node] = min(shortest_paths[next_node], new_dist)
            bisect.insort(node_queue, (new_dist, next_node))
    return min([val for node, val in shortest_paths.items() if node[0] == goal])
