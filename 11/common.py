def shortest_paths_sum(lines: list[str], mult: int) -> int:
    empty_rows: list[int] = [i for i, line in enumerate(lines) if all(ele != "#" for ele in list(line))]
    empty_cols: list[int] = [i for i in range(len(lines[0])) if all(lines[j][i] == "." for j in range(len(lines)))]

    galaxies: list[tuple[int, int]] = find_galaxies(lines)

    return sum([sum(dist(galaxies[i], galaxies[j], empty_rows, empty_cols, mult) for j in range(i + 1, len(galaxies)))
                for i in range(len(galaxies))])


def find_galaxies(lines: list[str]) -> list[tuple[int, int]]:
    galaxies: list[tuple[int, int]] = []
    for j in range(len(lines)):
        for i in range(len(lines[j])):
            if lines[j][i] == "#":
                galaxies.append((i, j))
    return galaxies


def dist(pos1: tuple[int, int], pos2: tuple[int, int], empty_rows: list[int], empty_cols: list[int], mult: int) -> int:
    empty_horiz = len([col for col in empty_cols if min(pos1[0], pos2[0]) < col < max(pos1[0], pos2[0])])
    empty_vert = len([row for row in empty_rows if min(pos1[1], pos2[1]) < row < max(pos1[1], pos2[1])])
    return abs(pos1[0] - pos2[0]) + empty_horiz * (mult - 1) + abs(pos1[1] - pos2[1]) + empty_vert * (mult - 1)
