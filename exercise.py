from utils.parse import get_parse, get_name


class Exercise:
    def __init__(self, line: str):
        self.name = get_name(line)
        self.text = ""
        self.sets = []
        self.include(line)

    def display(self):
        print(f"name = {self.name}")
        for s in self.sets:
            s.display()

    def include(self, line: str):
        """
        >>> exer = Exercise("Barbell back squat Warm-ups: Bodyweight squat 1x15, bar-1x10, 75lbs 1x5,".lower())
        >>> exer.display()
        name = barbell back squat
        {'weight': 'bodyweight', 'count': 1, 'reps': 15}
        {'weight': 'bar', 'count': 1, 'reps': 10}
        {'weight': 75.0, 'count': 1, 'reps': 5}
        >>> exer = Exercise("Conventional deadlift Warmup: 80lbs 1x5,".lower())
        >>> exer.display()
        name = conventional deadlift
        {'weight': 80.0, 'count': 1, 'reps': 5}
        >>> exer = Exercise("Flat barbell bench 2ct pause Build up to a Top set 3 at 115-125lbs depending on how you feel. Take as many warmups as needed. (don't forget to note how many from failure it was), then do 110lbs-4x4-5 (4 sets of 4-5 reps  backoff sets, 4 from failure goal for backoff sets)".lower())
        >>> exer.display()
        name = flat barbell bench
        {'weight': (115.0, 125.0), 'count': 1, 'reps': 3}
        {'weight': '110', 'count': 4, 'reps': (4, 5)}
        >>> exer = Exercise("Flat barbell bench 2ct pause Build up to a top set of 3 reps that is 4 from failure, then do 4x5 (4 sets of 5 reps) backoff sets -12% from the top set weight. My guess is your top set will be somewhere between 105-115lbs based on how you're feeling tomorrow".lower())
        >>> exer.display()
        name = flat barbell bench
        {'weight': (105.0, 115.0), 'count': 1, 'reps': 3}
        {'weight': (92.4, 101.2), 'count': 4, 'reps': 5}
        >>> exer = Exercise("flat barbell bench 2ct pause warm-ups bar 1x10, 65lbs 1x5 working sets: 95lbs 5x5 (pick weight based on how you feel today, (if detrained). goal for these sets is 3-4 from failure on each)")
        >>> exer.display()
        name = flat barbell bench
        {'weight': 'bar', 'count': 1, 'reps': 10}
        {'weight': 65.0, 'count': 1, 'reps': 5}
        {'weight': 95.0, 'count': 5, 'reps': 5}
        >>> exer = Exercise('barbell back squat warm-ups: bodyweight squat 1x15, bar-1x10, 75lbs 1x5, working sets: 100lbs 3x5')
        >>> exer.display()
        name = barbell back squat
        {'weight': 'bodyweight', 'count': 1, 'reps': 15}
        {'weight': 'bar', 'count': 1, 'reps': 10}
        {'weight': 75.0, 'count': 1, 'reps': 5}
        {'weight': 100.0, 'count': 3, 'reps': 5}
        """
        # update self.text
        if self.text:
            self.text = self.text + "\n" + line
        else:
            self.text = line

        parse = get_parse(line)
        self.sets += parse(line)
