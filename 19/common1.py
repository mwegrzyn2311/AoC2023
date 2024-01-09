import re
from typing import Callable

workflow_pattern: re.Pattern = re.compile('(?P<workflow_name>\w+){(?P<conditions>.+)}')
condition_pattern: re.Pattern = re.compile('(?P<category>\w+)(?P<operator>[<>])(?P<value>\d+):(?P<result>\w+)')


class Workflow:
    name: str
    conditions: list[Callable[[dict[str, int], int], bool]]
    # static
    workflows: dict = {}

    def __init__(self, workflow_str: str):
        workflow_match: re.Match = workflow_pattern.search(workflow_str)
        self.name = workflow_match.group('workflow_name')
        self.conditions = [self.__parse_condition(condition_str) for condition_str in workflow_match.group('conditions').split(',')]
        Workflow.workflows[self.name] = self

    def __parse_condition(self, condition_str: str) -> Callable[[dict[str, int], int], bool]:
        condition_match: re.Match = condition_pattern.search(condition_str)
        if condition_match:
            result = condition_match.group('result')
            if condition_match.group('operator') == '>':
                return lambda part, i: (True if result == 'A' else False if result == 'R' else Workflow.workflows[result].apply(part)) if part[condition_match.group('category')] > int(condition_match.group('value')) else self.conditions[i + 1](part, i + 1)
            elif condition_match.group('operator') == '<':
                return lambda part, i: (True if result == 'A' else False if result == 'R' else Workflow.workflows[result].apply(part)) if part[condition_match.group('category')] < int(condition_match.group('value')) else self.conditions[i + 1](part, i + 1)
        else:
            return lambda part, i: True if condition_str == 'A' else False if condition_str == 'R' else Workflow.workflows[condition_str].apply(part)

    def apply(self, part: dict[str, int]) -> bool:
        print(f'applying workflow {self.name} for part {part}')
        return self.conditions[0](part, 0)
