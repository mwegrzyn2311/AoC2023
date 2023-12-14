from utils.file_loader import load
from common import parse_mirrors, mirror_rows, mirror_cols


def main():
    solution(load('13.txt'))


def solution(lines: list[str]):
    print(sum([fix_smudge(mirror) for mirror in parse_mirrors(lines)]))


def fix_smudge(mirror: list[str]) -> int:
    col_res: int = fix_smudge_col(mirror)
    return col_res if col_res != 0 else fix_smudge_row(mirror)


def fix_smudge_col(mirror: list[str]) -> int:
    for i in range(len(mirror[0]) - 1):
        if fix_smudge_at_col(mirror, i):
            return i + 1
    return 0


def fix_smudge_at_col(mirror: list[str], col: int) -> bool:
    offset: int = 0
    smudge_at: tuple[int, int] = (-1, -1)
    while col - offset >= 0 and col + 1 + offset < len(mirror[0]):
        for y in range(len(mirror)):
            if mirror[y][col - offset] != mirror[y][col + 1 + offset]:
                if smudge_at == (-1, -1):
                    smudge_at = (col - offset, y)
                else:
                    return False
        offset += 1
    if smudge_at == (-1, -1):
        return False

    mirror[smudge_at[1]] = (mirror[smudge_at[1]][:smudge_at[0]] + mirror[smudge_at[1]][smudge_at[0] + 1]
                            + mirror[smudge_at[1]][smudge_at[0] + 1:])
    return True


def fix_smudge_row(mirror: list[str]) -> int:
    for i in range(len(mirror) - 1):
        if fix_smudge_at_row(mirror, i):
            return 100 * (i + 1)
    return 0


def fix_smudge_at_row(mirror: list[str], row: int) -> bool:
    offset: int = 0
    smudge_at: tuple[int, int] = (-1, -1)
    while row - offset >= 0 and row + 1 + offset < len(mirror):
        for x in range(len(mirror[0])):
            if not mirror[row - offset][x] == mirror[row + 1 + offset][x]:
                if smudge_at == (-1, -1):
                    smudge_at = (x, row - offset)
                else:
                    return False
        offset += 1

    if smudge_at == (-1, -1):
        return False
    mirror[smudge_at[1]] = (mirror[smudge_at[1]][:smudge_at[0]] + mirror[smudge_at[1] + 1][smudge_at[0]]
                            + mirror[smudge_at[1]][smudge_at[0] + 1:])
    return True


main()
