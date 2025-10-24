import random

def roll_2d6():
    return random.randint(1,6) + random.randint(1,6)

def roll_3d6():
    return random.randint(1,6) + random.randint(1,6) + random.randint(1,6)
