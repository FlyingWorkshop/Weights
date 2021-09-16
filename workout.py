from utils.exercise import Exercise
from utils.parse import process
from datetime import date
import string
import os
import json


class Workout:
    CACHE_FOLDER = "cache/"

    def __init__(self, filename: str):
        self.filename = filename
        self.date_cached = None
        data = process(filename)
        self.title = data["title"]
        self.exercises = []
        for line in data["lines"]:
            exer = Exercise(line)
            self.exercises.append(exer)

    def display(self) -> None:
        """
        NOTE: display does NOT display self.date_cached

        >>> workout = Workout("/Users/logan/PycharmProjects/Weights3/dev/top1.txt")
        >>> workout.display()
        ### filename = /Users/logan/PycharmProjects/Weights3/dev/top1.txt ###
        ### title = sunday combo workout ###
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
        >>> workout = Workout("/Users/logan/PycharmProjects/Weights3/dev/upper3.txt")
        >>> workout.display()
        ### filename = /Users/logan/PycharmProjects/Weights3/dev/upper3.txt ###
        ### title = wednesday or thursday full upper body workout ###
        name = flat dumbbell bench
        {'weight': 20.0, 'count': 1, 'reps': 10}
        {'weight': 30.0, 'count': 3, 'reps': (10, 12)}
        name = incline dumbbell chest supported rows
        {'weight': 30.0, 'count': 3, 'reps': 12}
        name = seated dumbbell shoulder press
        {'weight': 20.0, 'count': 3, 'reps': (8, 10)}
        name = dumbbell row
        {'weight': 30.0, 'count': 2, 'reps': 12}
        name = seated single arm overhead dumbbell triceps extension
        {'weight': 10.0, 'count': 4, 'reps': (12, 15)}
        name = seated lateral raises
        {'weight': 7.0, 'count': 4, 'reps': (12, 15)}
        name = seated dumbbell hammer curl
        {'weight': 15.0, 'count': 4, 'reps': (12, 15)}
        """
        print(f"### filename = {self.filename} ###")
        print(f"### title = {self.title} ###")
        for exer in self.exercises:
            exer.display()

    def cache_as_json(self):
        self.date_cached = str(date.today())
        cache_filename = self._make_cache_filename()
        data = self.to_dict()
        with open(cache_filename, 'w') as cf:
            json.dump(data, cf, indent=2)

    def _make_cache_filename(self) -> str:
        base = '_'.join(self.title.split())
        base.translate(str.maketrans('', '', string.punctuation))  # removes punctuation
        if "(" in base:
            base = base.split("(")[0].strip()

        i = 0
        cache_filename = f"{base}{i}.json"
        cache_dir = os.listdir(Workout.CACHE_FOLDER)
        while cache_filename in cache_dir:
            i += 1
            cache_filename = f"{base}{i}.json"
        return Workout.CACHE_FOLDER + cache_filename

    def to_dict(self) -> dict:
        """
        Converts all custom class objects (i.e. Set_ and Exercise) in this instance into dicts,
        so this instance can be cached as a JSON file.
        """
        data = {key: value for key, value in self.__dict__.items() if key != "exercises"}
        data["exercises"] = []
        for exer in self.exercises:
            exer_data = {key: value for key, value in exer.__dict__.items() if key != "sets"}
            exer_data["sets"] = []
            for set_ in exer.sets:
                exer_data["sets"].append(set_.__dict__)
            data["exercises"].append(exer_data)
        return data

