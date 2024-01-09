from utils.common import Vector2, Vector3


class Hailstorm2D:
    pos: Vector2
    vel: Vector2

    def __init__(self, pos: Vector2, vel: Vector2):
        self.pos = pos
        self.vel = vel

    def __str__(self):
        return f'pos: {self.pos}, vel: {self.vel}'

    def __repr__(self):
        return str(self)


class Hailstorm3D:
    pos: Vector3
    vel: Vector3

    def __init__(self, pos: Vector3, vel: Vector3):
        self.pos = pos
        self.vel = vel

    def to_2d(self) -> Hailstorm2D:
        return Hailstorm2D(self.pos.get_surf(), self.vel.get_surf())


def vec3_from_part(vec_str: str) -> Vector3:
    vec_parts: list[str] = vec_str.split(', ')
    return Vector3(int(vec_parts[0]), int(vec_parts[1]), int(vec_parts[2]))


def parse_hailstorms_p2(lines: list[str]) -> list[Hailstorm3D]:
    res: list[Hailstorm3D] = []
    for line in lines:
        parts: list[str] = line.split(' @ ')
        res.append(Hailstorm3D(vec3_from_part(parts[0]), vec3_from_part(parts[1])))
    return res


def parse_hailstorms_p1(lines: list[str]) -> list[Hailstorm2D]:
    return [h3d.to_2d() for h3d in parse_hailstorms_p2(lines)]

