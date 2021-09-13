from utils.set_ import Set_
from typing import Type, List
import re

INTERVAL = r"(\d+(?:-\d+)?)"


def get_name(line: str) -> str:
    """
    >>> get_name("Flat barbell bench 2ct pause Build up to a Top set 3 at 115-125lbs depending on how you feel. Take as many warmups as needed. (don't forget to note how many from failure it was), then do 110lbs-4x4-5 (4 sets of 4-5 reps  backoff sets, 4 from failure goal for backoff sets)".lower())
    'flat barbell bench'
    >>> get_name("V-ups 3x10 (moderate tempo on these)".lower())
    'v-ups'
    >>> get_name("Barbell back squat take your time warming up. Warm-ups: bar 1x10, 65lbs 1x5".lower())
    'barbell back squat'
    """
    name_words = []
    for word in line.split():
        if "take" in word or "warm" in word or has_digit(word):
            return ' '.join(name_words)
        name_words.append(word)


def get_weight(line: str) -> [str, float, tuple[float, float]]:
    """
    >>> get_weight("Dumbbell row 2ct pause at top 35lbs 2x8-10 3 from failure on each")
    35.0
    >>> get_weight("Dumbbell skull crushers 12lbs 3x12-15 1-2 from failure on each (last set with left arm only since it's weaker)")
    12.0
    >>> get_weight("bar 1x10")
    'bar'
    """
    for word in line.split():
        if word.endswith("lbs"):
            return convert(word.removesuffix("lbs"), float)
        elif word == "bar" or "bar-" in word:
            return "bar"
        elif word == "bodyweight" or "bodyweight-" in word:
            return "bodyweight"


def get_specs(line: str):
    """
    >>> get_specs("Incline dumbbell bench 25lbs each arm 3x8-10 3 from failure on each")
    (3, (8, 10))
    >>> get_specs("Seated lateral raises 10lbs 3x9")
    (3, 9)
    >>> get_specs("75lbs 1x5")
    (1, 5)
    """
    m = re.search(INTERVAL + "x" + INTERVAL, line)
    if m is None:
        return 0, 0
    count = convert(m.group(1), int)
    reps = convert(m.group(2), int)
    return count, reps


def make_set(line: str):
    weight = get_weight(line)
    count, reps = get_specs(line)
    return Set_(weight, count, reps)


def get_parse(lowercase: str):
    if is_topset(lowercase):
        return _parse_topset
    if is_warmup(lowercase):
        return _parse_warmup
    return _parse_simple


def is_warmup(lowercase: str) -> bool:
    return "warm" in lowercase


def is_topset(lowercase: str) -> bool:
    return "top set" in lowercase


def _parse_topset(line: str) -> list[Set_]:
    sets = []

    # get top set
    top = Set_()
    line = line[line.index("top set"):]
    words = line.split()
    top.reps = convert(get_first(has_digit, words), int)
    weights = re.findall(INTERVAL + "lbs", line)
    top.weight = convert(weights[0], float)
    top.count = 1
    sets.append(top)

    # get backoff set
    backoff = Set_()
    if "%" in line:
        multiplier = 1 + int(get_first(lambda s: "%" in s, words).removesuffix("%")) / 100
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


def _parse_warmup(line: str) -> list[Set_]:
    words = line.split()
    if ":" in line:
        line = line.split(":")[1]
    else:
        for i, word in enumerate(words):
            if is_warmup(word):
                line = ' '.join(words[i+1:])
    return [make_set(part) for part in line.split(",") if part]


def _parse_simple(line: str) -> list[Set_]:
    return [make_set(line)]


def has_digit(s: str) -> bool:
    return any(char.isdigit() for char in s)


def convert(s: str, cls: Type):
    """
    >>> convert('4', int)
    4
    >>> convert('4-5', int)
    (4, 5)
    """
    if s.startswith("-") or s.isnumeric():
        return cls(s)
    elif "-" in s:
        return tuple(map(cls, s.split("-")))
    return s


def get_first(func, iterable):
    for elem in iterable:
        if func(elem):
            return elem


def is_weight(s: str) -> bool:
    return s.endswith("lbs") or "bar" in s or "bodyweight" in s

