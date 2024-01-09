from utils.common import Vector2, Vector3, UNIT_3_Z, VEC_3_ONE


class Brick:
    low_corner: Vector3
    high_corner: Vector3
    supports: list
    supported_by: list

    def __init__(self, low_corner: Vector3, high_corner: Vector3):
        self.low_corner = low_corner
        self.high_corner = high_corner
        self.supports = []
        self.supported_by = []

    def move(self, vec3: Vector3):
        return Brick(self.low_corner - vec3, self.high_corner - vec3)

    def simple_str(self) -> str:
        return f'{self.low_corner} -> {self.high_corner}'

    def __str__(self):
        return f'{self.low_corner} -> {self.high_corner} ^ {[brick.simple_str() for brick in self.supports]} v {[brick.simple_str() for brick in self.supported_by]}'

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.low_corner == other.low_corner and self.high_corner == other.high_corner

    def __hash__(self):
        return hash(self.low_corner) * 13 + hash(self.high_corner) * 17

    def get_surf(self) -> tuple[Vector2, Vector2]:
        return Vector2(self.low_corner.x, self.low_corner.y), Vector2(self.high_corner.x, self.high_corner.y)


def vec3_from_str(vec3_str: str) -> Vector3:
    parts: list[int] = [int(part) for part in vec3_str.split(',')]
    return Vector3(parts[0], parts[1], parts[2])


def parse_brick(line: str) -> Brick:
    corners: list[str] = line.split('~')
    return Brick(vec3_from_str(corners[0]), vec3_from_str(corners[1]) + VEC_3_ONE)


def parse_bricks(lines: list[str]) -> list[Brick]:
    return sorted([parse_brick(line) for line in lines], key=lambda brick: brick.low_corner.z)


def surf_overlaps(surf1: tuple[Vector2, Vector2], surf2: tuple[Vector2, Vector2]) -> bool:
    return ((surf1[0].x < surf2[1].x and surf1[0].y < surf2[1].y and surf1[1].x > surf2[0].x and surf1[1].y > surf2[0].y)
            or (surf2[0].x < surf1[1].x and surf2[0].y < surf1[1].y and surf2[1].x > surf1[0].x and surf2[1].y > surf1[0].y))


def simulate_brick_falling(bricks: list[Brick]) -> list[Brick]:
    res: list[Brick] = []
    brick_tops: dict[int, list[Brick]] = {}
    for brick in bricks:
        brick_surf: tuple[Vector2, Vector2] = brick.get_surf()
        z: int = brick.low_corner.z
        bricks_supporting: list[Brick] = []
        while z > 1:
            if z in brick_tops:
                bricks_supporting = [brick_at_top for brick_at_top in brick_tops[z] if surf_overlaps(brick_surf, brick_at_top.get_surf())]
                if len(bricks_supporting) > 0:
                    break
            z -= 1
        new_brick: Brick = brick.move(UNIT_3_Z * (brick.low_corner.z - z))
        res.append(new_brick)
        if new_brick.high_corner.z not in brick_tops:
            brick_tops[new_brick.high_corner.z] = []
        brick_tops[new_brick.high_corner.z].append(new_brick)
        for brick_supporting in bricks_supporting:
            new_brick.supported_by.append(brick_supporting)
            brick_supporting.supports.append(new_brick)
    return sorted(res, key=lambda b: b.high_corner.z)


def how_many_can_be_deleted_v2(bricks: list[Brick]) -> int:
    return len([1 for brick in bricks if not any([len(another_brick.supported_by) == 1 for another_brick in bricks if another_brick is not brick and brick in another_brick.supported_by])])


def how_many_will_fall(bricks: list[Brick], brick: Brick) -> int:
    supporters: dict[Brick, tuple[list[Brick], list[Brick]]] = {b: ([x for x in b.supports], [x for x in b.supported_by]) for b in bricks}
    bricks_to_remove: list[Brick] = [brick]
    while len(bricks_to_remove) > 0:
        brick_to_remove: Brick = bricks_to_remove.pop()
        for supported in supporters[brick_to_remove][0]:
            supporters[supported][1].remove(brick_to_remove)
            if len(supporters[supported][1]) == 0:
                bricks_to_remove.append(supported)
        supporters[brick_to_remove][0].clear()
    return len([1 for b in supporters if b.low_corner.z != 1 and len(supporters[b][1]) == 0])


def how_many_will_fall_sum(bricks: list[Brick]) -> int:
    return sum([how_many_will_fall(bricks, brick) for brick in bricks])
