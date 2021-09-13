from utils.exercise import Exercise
from utils.parse import is_warmup
import string


class Workout:
    def __init__(self, filename: str):
        self.exercises = []
        with open(filename) as f:
            for line in f:
                line = line.strip().lower()
                if line and any(char.isdigit() for char in line):
                    exer = Exercise(line)
                    if is_warmup(line):
                        exer.include(next(f))
                    self.exercises.append(exer)

    def display(self):
        for exer in self.exercises:
            exer.display()
