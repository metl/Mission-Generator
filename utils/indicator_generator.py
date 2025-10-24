from tables.success_indicators import success_indicators_table
from tables.success_indicators import success_levels
import random

def roll_d66():
    """Roll a d66 (tens and ones). Returns an int like 11, 12, ..., 66."""
    tens = random.randint(1, 6)
    ones = random.randint(1, 6)
    return tens * 10 + ones

def generate_success_indicator():
    # Roll d66
    tens = random.randint(1,6)
    ones = random.randint(1,6)
    roll = tens*10 + ones
    # Fix roll if it becomes invalid (like 60, 0)
    if roll not in success_indicators_table:
        roll = 11  # fallback to first entry
    name = success_indicators_table[roll]

    # Assign level from success_levels table
    level = random.choice(success_levels)
    
    return {
        "name": name,
        "d66_roll": roll,
        "level": level["level"],
        "importance_roll": random.randint(1,6),
        "success_value": level["success_value"],
        "failure_value": level["failure_value"],
        }

def generate_success_indicators(num=5, max_paramount=1, max_important=1):
    indicators = []
    selected_keys = set()
    paramount_count = 0
    important_count = 0
    
    valid_keys = list(success_indicators_table.keys())
    if num > len(valid_keys):
        raise ValueError("Not enough indicators in the table to pick unique ones.")

    selected_keys = random.sample(valid_keys, num)

    for key in selected_keys:
        roll = random.randint(1, 6)
        if roll == 6 and paramount_count < max_paramount:
            level = "Paramount - Overrules all other indicators; this must succeed, even at other costs."
            success_value = 5
            failure_value = -12
            paramount_count += 1
        elif roll >= 5 and important_count < max_important:
            level = "Important - Primary Focus of Mission."
            success_value = 3
            failure_value = -4
            important_count += 1
        elif roll >= 4:
            level = "Critical - Failure could cause mission failure or major fallout."
            success_value = 4
            failure_value = -8
        else:
            level = "Routine - A nice-to-have condition; failure has minimal impact on mission success."
            success_value = 2
            failure_value = -2
        
        indicators.append({
            "name": success_indicators_table[key],
            "level": level,
            "success_value": success_value,
            "failure_value": failure_value
        })
    return indicators