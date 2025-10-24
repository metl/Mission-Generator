from utils.dice import roll_3d6
from tables.circumstances import unique_circumstances_table
import random
def generate_unique_circumstance():
    roll = roll_3d6()
    description = unique_circumstances_table.get(roll, "No special circumstance")
    return roll, description