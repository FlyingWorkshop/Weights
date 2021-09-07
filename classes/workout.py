from enum import Enum


class Workout:
    def __init__(self):
        self.title = ""
        self.date = None
        self.exercises_list = []


# TODO: (optional) figure out how to make docstring for classes
class Exercise:
    def __init__(self):
        self.unprocessed_line = ""
        self.name = ""
        self.weight = (0, 0)
        self.sets = []


class SetStyle(Enum):
    WARMUP = 0
    WORKING = 1
    TOP = 2


class Set_:
    def __init__(self, style: SetStyle, num_sets: tuple[int], num_reps: tuple[int]):
        self.style = style
        self.num_sets = num_sets
        self.num_reps = num_reps



