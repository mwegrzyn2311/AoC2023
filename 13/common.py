def parse_mirrors(lines: list[str]) -> list[list[str]]:
    mirrors: list[list[str]] = []
    mirror: list[str] = []
    for line in lines:
        if line.isspace():
            mirrors.append(mirror)
            mirror = []
        else:
            mirror.append(line[:-1])
    mirrors.append(mirror)
    return mirrors


def mirror_value(mirror: list[str]) -> int:
    print("-----")
    return mirror_value_col(mirror) + mirror_value_row(mirror)


def mirror_value_col(mirror: list[str]) -> int:
    col_values: list[int] = [(i + 1) for i in range(len(mirror[0]) - 1) if reflects_at_col(mirror, i)]
    return sum(col_values) if len(col_values) > 0 else 0


def mirror_cols(mirror: list[str]) -> list[int]:
    return [(i + 1) for i in range(len(mirror[0]) - 1) if reflects_at_col(mirror, i)]


def reflects_at_col(mirror: list[str], col: int) -> bool:
    offset: int = 0
    while col - offset >= 0 and col + 1 + offset < len(mirror[0]):
        if not cols_equal(mirror, col - offset, col + 1 + offset):
            return False
        offset += 1
    print(f'col {col}')
    return True


def cols_equal(mirror: list[str], col1: int, col2: int) -> bool:
    for y in range(len(mirror)):
        if mirror[y][col1] != mirror[y][col2]:
            return False
    return True


def mirror_value_row(mirror: list[str]) -> int:
    row_values: list[int] = [(i + 1) * 100 for i in range(len(mirror) - 1) if reflects_at_row(mirror, i)]
    return sum(row_values) if len(row_values) > 0 else 0


def mirror_rows(mirror: list[str]) -> list[int]:
    return [(i + 1) * 100 for i in range(len(mirror) - 1) if reflects_at_row(mirror, i)]


def reflects_at_row(mirror: list[str], row: int) -> bool:
    offset: int = 0
    while row - offset >= 0 and row + 1 + offset < len(mirror):
        if not mirror[row - offset] == mirror[row + 1 + offset]:
            return False
        offset += 1
    print(f'row {row}')
    return True
