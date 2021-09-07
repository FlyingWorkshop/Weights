from classes.parser import Parser


if __name__ == '__main__':
    parser = Parser()
    workout = parser.parse("classes/dev/combo1.txt")
    workout.display_workout()