from classes.workout import Workout, Exercise, SetStyle, Set_
from typing import Optional
import util
import re

INTERVAL = r"(\d+(?:-\d+)?)"
NAME = r"(\A.*?(?=\s\d))"
WEIGHT = fr"{INTERVAL}(?=lbs)"
SETS = fr"{INTERVAL}x{INTERVAL}"
EXERCISE_PATTERN = r".*?".join([NAME, WEIGHT, SETS])


class Parser:
    def parse(self, filename: str) -> Workout:
        """
        >>> p = Parser()
        >>> w = p.parse("dev/combo1.txt")
        >>> util.display(w)
        """
        workout = Workout()
        with open(filename) as f:
            workout.title = next(f)
            for line in f:
                line = line.strip()
                if not line or line.isalpha:
                    continue
                exercise = self.process(line)
                workout.exercises_list.append(exercise)
        return workout

    # TODO: handle edge case (1) ex's w/ warmups
    # TODO: handle edge case (2) ex's w/ complicated instructions (see doctest 3)
    @staticmethod
    def process(line: str) -> Optional[Exercise]:
        """
        >>> parser = Parser()
        >>> ex = parser.process("Seated hammer curl 20lbs 3x11-12 0-2 from failure on each")
        >>> util.display(ex)
        unprocessed_line = Seated hammer curl 20lbs 3x11-12 0-2 from failure on each
        name = Seated hammer curl
        weight = 20
        num_sets = 3
        num_reps = (11, 12)
        >>> ex = parser.process("Dumbbell row 2ct pause at top 35lbs 2x12")
        >>> util.display(ex)
        unprocessed_line = Dumbbell row 2ct pause at top 35lbs 2x12
        name = Dumbbell row
        weight = 35
        num_sets = 2
        num_reps = 12
        >>> ex = parser.process("Flat barbell bench 2ct pause Build up to a Top set 3 at 120lbs. Take as many warmups as needed. (don't forget to note how many from failure it was), then do 105lbs-4x5 backoff sets")
        >>> util.display(ex)
        unprocessed_line = Flat barbell bench 2ct pause Build up to a Top set 3 at 120lbs. Take as many warmups as needed. (don't forget to note how many from failure it was), then do 105lbs-4x5 backoff sets
        name = Flat barbell bench
        weight = 120
        num_sets = 1
        num_reps = 3
        """
        exercise = Exercise()
        m = re.search(EXERCISE_PATTERN, line)
        if m is None:
            return exercise
        exercise.unprocessed_line = line
        # TODO: determine ex. type (e.g. bar, body, dual, onehand)
        exercise.name = m.group(1)
        exercise.weight = util.convert(m.group(2))

        # TODO: determine set style rather than default to working
        s = Set_(SetStyle.WORKING, util.convert(m.group(3)), util.convert(m.group(4)))
        exercise.sets.append(s)
        return exercise
