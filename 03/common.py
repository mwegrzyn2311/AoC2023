class Coord:
    x: int
    y: int

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f'({self.x}, {self.y})'

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return 3 * self.x + 7 * self.y


class Engine:
    symbols: list[Coord]
    gears: list[Coord]
    numbers: dict[tuple[Coord, Coord], int]
    part_numbers_sum: int
    gear_neighbours: dict[Coord, list[int]]

    def __init__(self, symbols: list[Coord], numbers: dict[tuple[Coord, Coord], int], gears: list[Coord]):
        self.symbols = symbols
        self.numbers = numbers
        self.gears = gears
        self.part_numbers_sum = 0
        self.gear_neighbours = {}
        self.__analyze_part_numbers()

    def __analyze_part_numbers(self):
        for number_bounds in self.numbers:
            if self.is_part_number(number_bounds):
                self.part_numbers_sum += self.numbers[number_bounds]

    def is_part_number(self, number_bounds: tuple[Coord, Coord]) -> bool:
        res: bool = False
        if self.__check_symbol_mark_gear(Coord(number_bounds[0].x - 1, number_bounds[0].y), number_bounds):
            res = True
        if self.__check_symbol_mark_gear(Coord(number_bounds[1].x + 1, number_bounds[0].y), number_bounds):
            res = True
        y_above: int = number_bounds[0].y - 1
        y_below: int = y_above + 2
        for x in range(number_bounds[0].x - 1, number_bounds[1].x + 2):
            if self.__check_symbol_mark_gear(Coord(x, y_above), number_bounds):
                res = True
            if self.__check_symbol_mark_gear(Coord(x, y_below), number_bounds):
                res = True
        return res

    def __check_symbol_mark_gear(self, coord: Coord, number_bounds: tuple[Coord, Coord]):
        if coord in self.symbols:
            if coord in self.gears:
                if coord in self.gear_neighbours:
                    self.gear_neighbours[coord].append(self.numbers[number_bounds])
                else:
                    self.gear_neighbours[coord] = [self.numbers[number_bounds]]
            return True
        return False


def parse_engine(lines: list[str]) -> Engine:
    symbols: list[Coord] = []
    numbers: dict[tuple[Coord, Coord], int] = {}
    gears: list[Coord] = []
    curr_number: int = 0
    for j in range(len(lines)):
        line = lines[j]
        for i in range(len(line)):
            if line[i].isdigit():
                curr_number = curr_number * 10 + int(line[i])
            else:
                # Numbers equal to 0 don't add up to the sum, so we can ignore them
                if curr_number > 0:
                    numbers[(Coord(i - len(str(curr_number)), j), Coord(i - 1, j))] = curr_number
                    curr_number = 0
                if line[i] != '.' and line[i] != '\n':
                    symbols.append(Coord(i, j))
                    if line[i] == '*':
                        gears.append(Coord(i, j))

    return Engine(symbols, numbers, gears)
