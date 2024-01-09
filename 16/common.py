import copy
from utils.utils import str_insert


class Vector2:
    x: int
    y: int


    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y

    def is_in_map(self, width: int, height: int) -> bool:
        return 0 <= self.x < width and 0 <= self.y < height

    def is_vertical(self) -> bool:
        return self.x == 0

    def is_horizontal(self) -> bool:
        return self.y == 0

    def opposite_vectors(self):
        if self.x == 0:
            return [Vector2(-1, 0), Vector2(1, 0)]
        elif self.y == 0:
            return [Vector2(0, -1), Vector2(0, 1)]
        else:
            return []

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return self.x * 3 + self.y * 7

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return self.__str__()


class Beam:
    pos: Vector2
    direction: Vector2

    def __init__(self, pos: Vector2, direction: Vector2):
        self.pos = pos
        self.direction = direction

    # /
    def dir_after_forward_mirror(self) -> Vector2:
        return Vector2(-self.direction.y, -self.direction.x)

    # \
    def dir_after_backwards_mirror(self) -> Vector2:
        return Vector2(self.direction.y, self.direction.x)

    def move_to(self, new_pos: Vector2):
        self.pos = new_pos

    def __eq__(self, other) -> bool:
        return self.pos == other.pos and self.direction == other.direction

    def __hash__(self) -> int:
        return self.pos.__hash__() * 5 + self.direction.__hash__() * 11

    def __str__(self):
        return f'({self.pos} | {self.direction})'

    def __repr__(self):
        return self.__str__()


def simulate_beams(lines: list[str], starting_pos: Vector2, starting_dir: Vector2) -> int:
    beams: list[Beam] = [Beam(starting_pos, starting_dir)]
    if lines[starting_pos.y][starting_pos.x] == '\\':
        beams[0].direction = beams[0].dir_after_backwards_mirror()
    elif lines[starting_pos.y][starting_pos.x] == '/':
        beams[0].direction = beams[0].dir_after_forward_mirror()
    elif (lines[starting_pos.y][starting_pos.x] == '-' and beams[0].direction.is_vertical()) or (lines[starting_pos.y][starting_pos.x] == '|' and beams[0].direction.is_horizontal()):
        beam = beams.pop()
        for new_dir in beam.direction.opposite_vectors():
            beams.append(Beam(beam.pos, new_dir))
    global_pos_hist: dict[Beam, bool] = {}
    for beam in beams:
        global_pos_hist[Beam(beam.pos, beam.direction)] = True
    energized: dict[Vector2, bool] = {starting_pos: True}
    while len(beams) > 0:
        to_remove: list[Beam] = []
        to_add: list[Beam] = []
        for beam in beams:
            new_pos: Vector2 = beam.pos + beam.direction
            if not new_pos.is_in_map(len(lines[0]), len(lines)):
                to_remove.append(beam)
                continue
            energized[new_pos] = True
            beam.move_to(new_pos)
            tmp_beam: Beam = Beam(beam.pos, beam.direction)
            if tmp_beam in global_pos_hist:
                to_remove.append(beam)
                continue
            global_pos_hist[tmp_beam] = True
            curr_ele: str = lines[new_pos.y][new_pos.x]
            if (curr_ele == '-' and beam.direction.is_vertical()) or (
                    curr_ele == '|' and beam.direction.is_horizontal()):
                to_remove.append(beam)
                for new_dir in beam.direction.opposite_vectors():
                    to_add.append(Beam(beam.pos, new_dir))
            elif curr_ele == '/':
                beam.direction = beam.dir_after_forward_mirror()
            elif curr_ele == '\\':
                beam.direction = beam.dir_after_backwards_mirror()

        for beam in to_remove:
            beams.remove(beam)
        for beam in to_add:
            beams.append(beam)

    return len(energized)


def print_map(lines: list[str], energized: dict[Vector2, bool]):
    print(energized)
    tmp_lines: list[str] = copy.deepcopy(lines)
    for pos in energized:
        tmp_lines[pos.y] = str_insert(tmp_lines[pos.y], pos.x, '#')
    for line in tmp_lines:
        print(line)
