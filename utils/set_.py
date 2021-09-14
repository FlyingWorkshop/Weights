class Set_:
    def __init__(self, weight=None, count=None, reps=None):
        self.weight = weight
        self.count = count
        self.reps = reps

    def display(self):
        print(self.__dict__)
