from enum import IntEnum
from copy import deepcopy
import json
import networkx as nx

from utils.graph import GraphVisualization


class Pulse(IntEnum):
    HIGH = 1
    LOW = 2
    NONE = 3


class Module:
    name: str
    outputs: list[str]

    def __init__(self, name:str, outputs: list[str]):
        self.name = name
        self.outputs = outputs

    def consume_pulse(self, pulse: Pulse, input_name: str) -> Pulse:
        return Pulse.NONE

    def copy(self):
        pass

    def __eq__(self, other):
        return type(self) is type(other) and self.name == other.name

    def __hash__(self):
        return hash((type(self), self.name))

    def __str__(self):
        return f'{type(self)}({self.name})'

    def __repr__(self):
        return self.__str__()


class Broadcaster(Module):
    def __init__(self, name:str, outputs: list[str]):
        super().__init__(name, outputs)

    # Override
    def consume_pulse(self, pulse: Pulse, input_name: str) -> Pulse:
        return pulse

    # Override
    def copy(self):
        return Broadcaster(self.name, [])

    def __repr__(self):
        return super().__repr__()


class FlipFlop(Module):
    on: bool

    def __init__(self, name:str, outputs: list[str]):
        super().__init__(name, outputs)
        self.on = False

    # Override
    def consume_pulse(self, pulse: Pulse, input_name: str) -> Pulse:
        if pulse == Pulse.LOW:
            self.on = not self.on
            return Pulse.HIGH if self.on else Pulse.LOW
        return Pulse.NONE

    # Override
    def copy(self):
        copy = FlipFlop(self.name, [])
        copy.on = self.on
        return copy

    def __eq__(self, other):
        return super().__eq__(other) and self.on == other.on

    def __hash__(self):
        return hash((super().__hash__(), self.on))

    # Override
    def __str__(self):
        return f'{super().__str__()}: {self.on}'

    def __repr__(self):
        return super().__repr__()


class Conjunction(Module):
    inputs_pulses: dict[str, Pulse]
    on: bool
    once_on: bool

    def __init__(self, name: str, outputs: list[str]):
        super().__init__(name, outputs)
        self.inputs_pulses = {}
        self.on = False
        self.once_on = False

    def register_input(self, input_name: str):
        self.inputs_pulses[input_name] = Pulse.LOW

    # Override
    def consume_pulse(self, pulse: Pulse, input_name: str) -> Pulse:
        self.inputs_pulses[input_name] = pulse
        self.on = all([pulse == Pulse.HIGH for pulse in self.inputs_pulses.values()])
        if self.on:
            self.once_on = True
            return Pulse.LOW
        else:
            return Pulse.HIGH

    # Override
    def copy(self):
        copy = Conjunction(self.name, [])
        copy.inputs_pulses = deepcopy(self.inputs_pulses)
        return copy

    def __eq__(self, other):
        return super().__eq__(other) and self.inputs_pulses == other.inputs_pulses

    def __hash__(self):
        return hash((super().__hash__(), json.dumps(self.inputs_pulses, sort_keys=True)))

    # Override
    def __str__(self):
        return f'{super().__str__()}: {self.inputs_pulses}'

    def __repr__(self):
        return super().__repr__()


class RX(Module):
    on: bool

    def __init__(self, name: str, outputs: list[str]):
        super().__init__(name, outputs)
        self.on = False
        self.low_pulses = 0

    def consume_pulse(self, pulse: Pulse, input_name: str) -> Pulse:
        if pulse == Pulse.LOW:
            print("Consumed low pulse")
            self.on = True


class Controller:
    cycles: int
    pulses: dict[Pulse, list[int]]
    modules: dict[str, Module]
    previous_states: set[tuple]

    def __init__(self):
        self.cycles = 0
        self.pulses = {Pulse.LOW: [], Pulse.HIGH: []}
        self.modules = {}

    def play_until_repeat(self):
        self.previous_states = {tuple([module.copy() for module_name, module in self.modules.items()])}
        while self.button() and self.cycles < 1000:
            print(f'----{self.cycles}----')
            if self.cycles == 940:
                print(self.modules['qr'].inputs_pulses)

    def play_until_module_on(self, module_name: str):
        self.previous_states = {tuple([module.copy() for module_name, module in self.modules.items()])}
        while self.button() and not self.modules[module_name].once_on:
            if self.cycles % 10000 == 0:
                print(self.cycles)

    def play_until_rx_on(self):
        self.previous_states = {tuple([module.copy() for module_name, module in self.modules.items()])}
        while self.button() and not self.modules['rx'].on:
            if self.cycles % 10000 == 0:
                print(self.cycles)

    def button(self) -> bool:
        queue: list[tuple[str, Pulse, str]] = [('broadcaster', Pulse.LOW, 'button')]
        self.pulses[Pulse.LOW].append(0)
        self.pulses[Pulse.HIGH].append(0)
        while len(queue) > 0:
            module_name, pulse, input_name = queue.pop(0)
            #print(f"{input_name} -{'high' if pulse == Pulse.HIGH else 'low' if pulse == Pulse.LOW else '???'}-> {module_name}")
            self.pulses[pulse][self.cycles] += 1
            if module_name not in self.modules:
                continue
            module: Module = self.modules[module_name]
            new_pulse: Pulse = module.consume_pulse(pulse, input_name)
            if new_pulse != Pulse.NONE:
                for output in module.outputs:
                    queue.append((output, new_pulse, module_name))
        self.cycles += 1
        state: tuple = tuple([module.copy() for module_name, module in self.modules.items()])
        if state not in self.previous_states:
            self.previous_states.add(state)
            return True
        else:
            return False


def parse_modules(lines: list[str]) -> Controller:
    controller = Controller()
    g_viz = GraphVisualization()
    for line in lines:
        input_outputs: list[str] = line.split(" -> ")
        module: Module = module_from_str(input_outputs[0], input_outputs[1].strip('\n').split(", "))
        controller.modules[module.name] = module
    controller.modules['rx'] = RX('rx', [])
    for module_name, module in controller.modules.items():
        if type(module) is Conjunction:
            for potential_input_name, potential_input in controller.modules.items():
                if module_name in potential_input.outputs:
                    module.register_input(potential_input_name)
                    g_viz.add_edge(potential_input_name, module_name)
    #g_viz.visualize_directed()

    return controller


def module_from_str(input_str: str, outputs: list[str]) -> Module:
    if input_str == 'broadcaster':
        return Broadcaster(input_str, outputs)
    else:
        module_type: str = input_str[0]
        if module_type == '%':
            return FlipFlop(input_str[1:], outputs)
        elif module_type == '&':
            return Conjunction(input_str[1:], outputs)
        else:
            print(input_str)
            print('ERR: unknown type')
