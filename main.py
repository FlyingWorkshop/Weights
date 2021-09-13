from utils.workout import Workout
import os


def main():
    for filename in os.listdir("dev"):
        workout = Workout(f"dev/{filename}")
        workout.display()
        print(filename)


if __name__ == '__main__':
    main()
