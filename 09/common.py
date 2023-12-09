def parse_nums(lines: list[str]) -> list[list[list[int]]]:
    res: list[list[list[int]]] = []
    for line in lines:
        numbers: list[list[int]] = [[int(num) for num in line.split()]]
        while not all(num == numbers[-1][0] for num in numbers[-1]):
            numbers.append([numbers[-1][i] - numbers[-1][i-1] for i in range(1, len(numbers[-1]))])
        res.append(numbers)
    return res
