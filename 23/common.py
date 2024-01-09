from utils.common import Vector2, NEIGH_DIRS, DOWN, LEFT, UP, RIGHT


SLOPES: dict[str, Vector2] = {
    '>': RIGHT,
    'v': DOWN,
    '<': LEFT,
    '^': UP
}


def transform_into_graph(lines: list[str], ignore_slopes: bool = False) -> dict[Vector2, set[tuple[Vector2, int]]]:
    start: Vector2 = Vector2(lines[0].index('.'), 0)
    graph: dict[Vector2, set[tuple[Vector2, int]]] = {start: set()}
    pos_stack: list[tuple[Vector2, Vector2]] = [(start, start + DOWN)]
    visited_edge_starts: set[Vector2] = set()
    while len(pos_stack) > 0:
        last_node, curr_pos = pos_stack.pop(0)
        edge_len: int = 1
        if curr_pos in visited_edge_starts:
            # Has already been reached by another route
            continue
        visited_edge_starts.add(curr_pos)
        double_oriented: bool = True
        same_orientation: bool = True
        last_dir_rev: Vector2 = last_node - curr_pos
        unvisited_neighs: list[Vector2] = []
        curr_char: str = lines[curr_pos.y][curr_pos.x]
        if not ignore_slopes and curr_char in SLOPES:
            double_oriented = False
            same_orientation = (last_dir_rev != SLOPES[curr_char])
        while True:
            if curr_pos.y == len(lines) - 1:
                break
            for neigh_dir in NEIGH_DIRS:
                neigh_pos: Vector2 = curr_pos + neigh_dir
                curr_char: str = lines[neigh_pos.y][neigh_pos.x]
                if last_dir_rev != neigh_dir and curr_char != '#':
                    unvisited_neighs.append(neigh_pos)
                    if not ignore_slopes and curr_char in SLOPES:
                        if double_oriented:
                            double_oriented = False
                            same_orientation = (last_dir_rev != SLOPES[curr_char])
            if len(unvisited_neighs) > 1:
                break
            next_pos = unvisited_neighs.pop()
            last_dir_rev = curr_pos - next_pos
            curr_pos = next_pos
            edge_len += 1
            if curr_pos in graph:
                break
        if curr_pos not in graph:
            graph[curr_pos] = set()
        if double_oriented:
            graph[last_node].add((curr_pos, edge_len))
            graph[curr_pos].add((last_node, edge_len))
        elif same_orientation:
            graph[last_node].add((curr_pos, edge_len))
        else:
            graph[curr_pos].add((last_node, edge_len))
        for node in unvisited_neighs:
            pos_stack.append((curr_pos, node))
    return graph


def longest_path(graph: dict[Vector2, set[tuple[Vector2, int]]], curr_pos: Vector2, curr_dist: int, visited: list[Vector2], end: Vector2) -> int:
    if curr_pos in visited:
        return -1
    if curr_pos == end:
        return curr_dist
    return max([longest_path(graph, new_pos, curr_dist + dist, visited + [curr_pos], end) for new_pos, dist in graph[curr_pos]])
