from utils.exercise import Exercise
from utils.parse import process


class Workout:
    def __init__(self, filename: str):
        self.filename = filename
        self.exercises = []
        lines = process(filename)
        for line in lines:
            exer = Exercise(line)
            self.exercises.append(exer)

    def display(self):
        """
        >>> workout = Workout("/Users/logan/PycharmProjects/Weights3/dev/top1.txt")
        >>> workout.display()
        ### filename = /Users/logan/PycharmProjects/Weights3/dev/top1.txt ###
        name = barbell back squat
        {'weight': 'bodyweight', 'count': 1, 'reps': 15}
        {'weight': 'bar', 'count': 1, 'reps': 10}
        {'weight': 75.0, 'count': 1, 'reps': 5}
        {'weight': 100.0, 'count': 3, 'reps': 5}
        name = conventional deadlift
        {'weight': 80.0, 'count': 1, 'reps': 5}
        {'weight': (100.0, 105.0), 'count': 2, 'reps': 5}
        name = flat barbell bench
        {'weight': (115.0, 125.0), 'count': 1, 'reps': 3}
        {'weight': '110', 'count': 4, 'reps': (4, 5)}
        name = bulgarian split squat
        {'weight': 5.0, 'count': 3, 'reps': (12, 15)}
        name = v-ups
        {'weight': None, 'count': 3, 'reps': 10}
        name = incline dumbbell chest supported row
        {'weight': 30.0, 'count': 2, 'reps': (10, 12)}
        name = incline dumbbell bench
        {'weight': 25.0, 'count': 3, 'reps': (10, 14)}
        name = dumbbell row
        {'weight': 35.0, 'count': 2, 'reps': (10, 12)}
        name = seated lateral raises
        {'weight': 7.0, 'count': 4, 'reps': (10, 15)}
        name = dumbbell skull crushers
        {'weight': 12.0, 'count': 4, 'reps': (12, 15)}
        name = seated hammer curl
        {'weight': 20.0, 'count': 3, 'reps': (10, 15)}
        """
        print(f"### filename = {self.filename} ###")
        for exer in self.exercises:
            exer.display()
