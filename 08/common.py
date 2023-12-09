import re

node_pattern = '(?P<curr_label>\w\w\w)\s+=\s+\((?P<left_label>\w\w\w), (?P<right_label>\w\w\w)\)'


def parse_nodes(lines: list[str]) -> dict[str, tuple[str, str]]:
    nodes: dict[str, tuple[str, str]] = {}
    for i in range(2, len(lines)):
        node_match = re.search(node_pattern, lines[i])
        nodes[node_match.group('curr_label')] = (node_match.group('left_label'), node_match.group('right_label'))
    return nodes
