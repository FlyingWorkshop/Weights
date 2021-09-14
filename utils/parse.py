from utils.set_ import Set_
from typing import Type
import re

INTERVAL = r"(\d+(?:-\d+)?)"


def process(filename: str) -> list[str]:
    """
    The purpose of this method is to weed out bad lines (e.g. title, blanks, etc.) and
    also to group relevant lines together (e.g. lines about the same exercise)
    """
    with open(filename) as f:
        raw_lines = [line.strip().lower() for line in f if line and has_digit(line)]
    cooked_lines = []
    i = 0
    while i < len(raw_lines):
        line = raw_lines[i]
        if is_topset(line) or is_warmup(line):
            succ = raw_lines[i+1]
            if is_homoousian(succ):
                i += 1
                line = line + " " + succ
        cooked_lines.append(line)
        i += 1
    return cooked_lines


def get_name(line: str) -> str:
    """
    Extracts the exercise name from the input string.
    >>> get_name("Flat barbell bench 2ct pause Build up to a Top set 3 at 115-125lbs depending on how you feel. Take as many warmups as needed. (don't forget to note how many from failure it was), then do 110lbs-4x4-5 (4 sets of 4-5 reps  backoff sets, 4 from failure goal for backoff sets)".lower())
    'flat barbell bench'
    >>> get_name("V-ups 3x10 (moderate tempo on these)".lower())
    'v-ups'
    >>> get_name("Barbell back squat take your time warming up. Warm-ups: bar 1x10, 65lbs 1x5".lower())
    'barbell back squat'
    """
    if "plank" in line:
        return "plank"
    name_words = []
    for word in line.split():
        if "take" in word or "warm" in word or has_digit(word):
            return ' '.join(name_words)
        name_words.append(word)


def get_weight(line: str) -> [str, float, tuple[float, float]]:
    """
    Extracts the exercise weight from the input string.
    >>> get_weight("Dumbbell row 2ct pause at top 35lbs 2x8-10 3 from failure on each")
    35.0
    >>> get_weight("Dumbbell skull crushers 12lbs 3x12-15 1-2 from failure on each (last set with left arm only since it's weaker)")
    12.0
    >>> get_weight("bar 1x10")
    'bar'
    >>> get_weight("10-20lbs")
    (10.0, 20.0)
    """
    for word in line.split():
        if word.endswith("lbs"):
            m = re.search(INTERVAL, word)
            if m is not None:
                return convert(m.group(1).removesuffix("lbs"), float)
        elif word == "bar" or "bar-" in word:
            return "bar"
        elif word == "bodyweight" or "bodyweight-" in word:
            return "bodyweight"


def get_specs(line: str):
    """
    Extracts the count and reps from the input string.
    >>> get_specs("Incline dumbbell bench 25lbs each arm 3x8-10 3 from failure on each")
    (3, (8, 10))
    >>> get_specs("Seated lateral raises 10lbs 3x9")
    (3, 9)
    >>> get_specs("75lbs 1x5")
    (1, 5)
    >>> get_specs("Bulgarian split squat 5lbs each hand 3 sets of 15")
    (3, 15)
    >>> get_specs("Bulgarian split squat 5lbs each hand 3 sets of 12-15 3 from failure on each")
    (3, (12, 15))
    >>> get_specs("plank one set of 1min. 15 secs")
    (None, None)
    """
    m = re.search(INTERVAL + "x" + INTERVAL, line)
    if m is None and "sets of" in line:
        m = re.search(INTERVAL + "\ssets of\s" + INTERVAL, line)

    if m is None:
        count = None
        reps = None
    else:
        count = convert(m.group(1), int)
        reps = convert(m.group(2), int)
    return count, reps


def make_set(line: str):
    """
    Creates and returns a Set_ objected with information parsed from the input string.
    >>> make_set("100lbs 3x10").display()
    {'weight': 100.0, 'count': 3, 'reps': 10}
    >>> make_set("Working sets: 100lbs 3x5").display()
    {'weight': 100.0, 'count': 3, 'reps': 5}
    >>> make_set(" working sets:100-105lbs 2x5").display()
    {'weight': (100.0, 105.0), 'count': 2, 'reps': 5}
    >>> make_set("s: 95lbs 5x5 (pick weight based on how you feel today").display()
    {'weight': 95.0, 'count': 5, 'reps': 5}
    >>> make_set("plank one set of 1min. 15 secs").display()
    {'weight': None, 'count': None, 'reps': None}
    """
    weight = get_weight(line)
    count, reps = get_specs(line)
    return Set_(weight, count, reps)


def get_parse(lowercase: str):
    """
    Factory function that returns different parsing routines
    """
    if is_topset(lowercase):
        return _parse_topset
    if is_warmup(lowercase):
        return _parse_warmup
    return _parse_simple


def is_warmup(line: str) -> bool:
    return "warm" in line


def is_topset(line: str) -> bool:
    """
    >>> is_topset("barbell back squat build up to a top set of 3 reps, 4 from failure. then do 3x5 backoff sets -18-22% off the top set weight. goal for these is 4-5 reps from failure so pick weight accordingly.")
    True
    """
    return "top set" in line


def is_homoousian(line: str) -> bool:
    """
    In use, returns whether a given line is related to another. For example, if both the previous and current lines
    have information about the same exercise, then this returns true. The function doesn't actually check the content
    of the line; rather, it's based on ad-hoc observations on my trainer's rhetorical patterns.

    >>> is_homoousian("(probably somewhere between 90-110lbs for top set based on how you're feeling tomorrow.)")
    True
    """
    enclosed = line.startswith("(") and line.endswith(")")
    is_workset = "working set" in line
    return enclosed or is_workset


def _parse_topset(line: str) -> list[Set_]:
    """
    >>> l = _parse_topset("Barbell back squat Build up to a top set of 3 reps, 4 from failure. Then do 3x5 backoff sets -18-22% off the top set weight. Goal for these is 4-5 reps from failure so pick weight accordingly. (Probably somewhere between 90-110lbs for top set based on how you're feeling tomorrow.)".lower())
    >>> l[0].display()
    {'weight': (90.0, 110.0), 'count': 1, 'reps': 3}
    >>> l[1].display()
    {'weight': (73.80000000000001, 90.2), 'count': 3, 'reps': 5}
    """
    sets = []

    # get top set
    top = Set_()
    line = line[line.index("top set"):]
    words = line.split()
    top.reps = convert(get_first(has_digit, words), int)
    weights = re.findall(INTERVAL + "lbs", line)
    # TODO: maybe remove this later
    # if not weights:
    #     return _manual_input(line)
    top.weight = convert(weights[0], float)
    top.count = 1
    sets.append(top)

    # get backoff set
    backoff = Set_()
    if "%" in line:
        percent = convert(get_first(lambda s: "%" in s, words).removesuffix("%"), float)
        if isinstance(percent, tuple):
            percent = percent[0]
        multiplier = 1 + percent / 100
        if isinstance(top.weight, float):
            backoff.weight = top.weight * multiplier
        else:
            backoff.weight = tuple(n * multiplier for n in top.weight)
    else:
        backoff.weight = weights[1]
    count, reps = get_specs(line)
    backoff.count = count
    backoff.reps = reps
    sets.append(backoff)
    return sets


def _manual_input(line: str) -> list[Set_]:
    print(f"Couldn't parse: \n\t '{line}'")
    print("Please manually enter set data. (e.g. '100lbs 3x10, 105lbs 2x4')")
    user_input = input(f"Enter set data: ")
    if "," in user_input:
        return [make_set(part) for part in user_input.split(",") if part]
    else:
        return [make_set(user_input)]


def _parse_warmup(line: str) -> list[Set_]:
    # exclude everything before warmup (e.g. exercise name)
    # this is needed since the exercise name may have a number in it (e.g. '2ct')
    words = line.split()
    for i, word in enumerate(words):
        if is_warmup(word):
            line = ' '.join(words[i+1:])
            break

    sets = []
    parts = [line for line in line.split(",") if line and has_digit(line) and has_weight(line)]
    for part in parts:
        if part.count("x") + part.count("sets of") > 1:
            # TODO: change below
            subpart1, subpart2 = part.split("sets:")
            sets += [make_set(subpart1), make_set(subpart2)]
        else:
            sets.append(make_set(part))
    return sets


def _parse_simple(line: str) -> list[Set_]:
    return [make_set(line)]


def convert(s: str, cls: Type):
    """
    >>> convert('4', int)
    4
    >>> convert('4-5', int)
    (4, 5)
    >>> convert('-10-15', float)
    (-10.0, -15.0)
    """
    if s.isnumeric():
        return cls(s)
    elif s.startswith("-"):
        if s.count("-") == 1:
            return cls(s)
        else:
            return tuple([-1 * cls(elem) for elem in s.split("-") if elem])
    elif "-" in s:
        return tuple(map(cls, s.split("-")))
    return s


def get_first(func, iterable):
    for elem in iterable:
        if func(elem):
            return elem


def has_weight(s: str) -> bool:
    return any(substring in s for substring in ["bar", "lbs", "bodyweight"])


def has_interval(s: str) -> bool:
    return re.search(INTERVAL, s) is not None


def has_digit(s: str) -> bool:
    return any(char.isdigit() for char in s)