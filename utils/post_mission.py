from tables.outcomes import post_mission_outcome_table
from utils.dice import roll_2d6
import random
def generate_post_mission_outcome():
    roll = random.randint(1,6)
    outcome = post_mission_outcome_table.get(roll, "No special outcome")
    is_branch = roll == 6
    return roll, outcome, is_branch