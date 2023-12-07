import re

game_pattern = 'Game (?P<game_no>\d+): (?P<game_sets>.*)'
cube_pattern = '(?P<cubes_no>\d+) (?P<color>blue|red|green)'


def parse_games(lines: list[str]) -> dict[int, dict[str, int]]:
    games: dict[int, dict[str, int]] = {}
    for line in lines:
        game_match = re.search(game_pattern, line)
        game: dict[str, int] = {}
        for game_set in game_match.group('game_sets').split('; '):
            cubes: list[str] = game_set.split(', ')
            for cube in cubes:
                cube_match = re.search(cube_pattern, cube)
                cubes_no: int = int(cube_match.group('cubes_no'))
                cubes_color: str = cube_match.group('color')
                game[cubes_color] = max(game[cubes_color], cubes_no) if cubes_color in game else cubes_no
        games[int(game_match.group('game_no'))] = game
    return games
