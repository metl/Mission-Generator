import random

# ------------------ Tables ------------------
objectives_table = {
    2: "Assassinate / Sabotage",
    3: "Attack / Raid",
    4: "Defend / Guard",
    5: "Negotiate / Broker / Diplomacy",
    6: "Escort / Protect",
    7: "Transport (cargo, passengers, or mail)",
    8: "Recover / Rescue",
    9: "Locate / Discover",
    10: "Investigate / Observe",
    11: "Explore / Survey",
    12: "One-Off (prototype test, strange request)"
}

targets_table = {
    2: ("Small Gang", 0),
    3: ("Corporate Facility", 1),
    4: ("Pirate Base", 2),
    5: ("Rival Faction", 2),
    6: ("Individual VIP", 1),
    7: ("Smuggling Ring", 1),
    8: ("Research Station", 2),
    9: ("Military Outpost", 3),
    10: ("Alien Artifact", 4),
    11: ("Ancient Ruins", 3),
    12: ("Unknown Entity", 4)
}

distance_table = {
    2: ("Same Planet", "Local"),
    3: ("Nearby Planet", "Local"),
    4: ("Nearby Planet", "Local"),
    5: ("1x Jump Rating", "Near"),
    6: ("1x Jump Rating", "Near"),
    7: ("1x Jump Rating", "Near"),
    8: ("2x Jump Rating", "Distant"),
    9: ("2x Jump Rating", "Distant"),
    10: ("3x Jump Rating", "Far"),
    11: ("3x Jump Rating", "Far"),
    12: ("4x Jump Rating", "Extreme")
}

world_table = {
    2: (-2, "Barren / Asteroid", "mining, salvage, or survey missions"),
    3: (-2, "Barren / Asteroid", "mining, salvage, or survey missions"),
    4: (-1, "Outpost / Minor Colony", "Small population"),
    5: (-1, "Outpost / Minor Colony", "Small population"),
    6: (0, "Industrial / Mining", "Factories, mines; moderate hazards, crime"),
    7: (0, "Industrial / Mining", "Factories, mines; moderate hazards, crime"),
    8: (0, "Agricultural / Farming", "Farms or colonists"),
    9: (+1, "Civilized / Moderate Tech", "Fully populated"),
    10: (+2, "Advanced / High-Tech", "Tech hubs, labs"),
    11: (+3, "Amber / Exotic World", "Exploration, first contact, caution advised"),
    12: (+4, "X-Red Zone", "Conflict-heavy; extremely hazardous")
}

# Success indicators (example, values can be expanded)
success_indicators_table = {
    11: "Avoid Conflict", 
    12: "Locate Target", 
    13: "Retrieve Item", 
    14: "Protect Asset", 
    15: "Evade Detection", 
    16: "Negotiate Outcome",
    21: "Complete on Schedule", 
    22: "Minimize Damage", 
    23: "Gather Intelligence", 
    24: "Secure Area", 
    25: "Deliver Cargo", 
    26: "Disable Systems",
    31: "Extract Target", 
    32: "No Survivors", 
    33: "Acquire Target", 
    34: "Investigate", 
    35: "Escort Target", 
    36: "Neutralize Threat",
    41: "Maintain Cover", 
    42: "Transmit Information", 
    43: "Repair / Restore", 
    44: "Survey Area", 
    45: "Collect Samples", 
    46: "Defend Asset",
    51: "Avoid Law / Security", 
    52: "Complete Main Objective", 
    53: "Analyze Data", 
    54: "Coordinate Parties", 
    55: "Contain Hazard", 
    56: "Recover Evidence",
    61: "Reveal Hidden", 
    62: "Maintain Morale", 
    63: "Establish Communication", 
    64: "Adapt to Change", 
    65: "Achieve Objectives", 
    66: "No Casualties"
}

success_levels = [
    {"level": "Routine - A nice-to-have condition; failure has minimal impact on mission success.", "success_value": 2, "failure_value": -2},
    {"level": "Important - Primary Focus of Mission", "success_value": 3, "failure_value": -4},
    {"level": "Critical - Failure could cause mission failure or major fallout.", "success_value": 4, "failure_value": -8},
    {"level": "Paramount - Overrules all other indicators; this must succeed, even at other costs.", "success_value": 5, "failure_value": -12}
]

# Unique circumstance table (3d6)
unique_circumstances_table = {
    3: "Time-Sensitive: Mission must be completed quickly; penalties for delay",
    4: "Undercover / Covert: Stealth required; high risk if discovered",
    5: "Competing Faction: Another group is attempting the same mission",
    6: "Environmental Hazard: Weather, dangerous terrain, or unstable systems",
    7: "Political / Diplomatic Pressure: High stakes due to politics or treaties",
    8: "Limited Resources: Crew or equipment is insufficient; improvisation needed",
    9: "Set-Up / Ambush: Mission is a trap or someone is manipulating events",
    10: "High Profile / VIP Involvement: Success/failure has major consequences",
    11: "Unusual Technology / Experimental: Requires special equipment or skills",
    12: "Moral / Ethical Dilemma: Choice affects reputation, faction alignment, or lives",
    13: "Hostile Locals: Indigenous or native groups may interfere",
    14: "Enemy Patrols: Mission area actively patrolled by hostile forces",
    15: "Communication Blackout: Limited or no contact with allies",
    16: "Sabotage / Countermeasures: Enemy or Rival actively obstructs mission",
    17: "Unstable Cargo: Mission involves dangerous, fragile, or volatile materials",
    18: "Unexpected Ally / Rival: A mysterious faction intervenes, helping or hindering"
}

# Each entry: (min_total, max_total, payout)
payout_table = [
    (6, 9, 25000),
    (10, 10, 50000),
    (11, 11, 75000),
    (12, 12, 100000),
    (13, 13, 125000),
    (14, 14, 150000),
    (15, 15, 175000),
    (16, 16, 200000),
    (18, 19, 225000),
    (20, float('inf'), 250000),  # 20+
]

# Post-mission outcomes (2d6)
post_mission_outcome_table = {
    2: "Twist: Patron changes terms (good or bad). Success Indicators and payout changes.",
    3: "Patron adds new objective, D3 Success Indicators, no additional pay.",
    4: "Patron adds new objective, D3 Success Indicators, no additional pay.",
    5: "Mission Ends — Return to Patron.",
    6: "Mission Ends — Return to Patron.",
    7: "Mission Ends — Return to Patron.",
    8: "Mission Ends — Return to Patron.",
    9: "Mission Ends — Return to Patron.",
    10: "Branch — D3 New Objectives, D3 additional Success Indicators added to base TSI. Roll Distance with DM–4.",
    11: "Branch — D3 New Objectives, D3 additional Success Indicators added to base TSI. Roll Distance with DM–4.",
    12: "Branch — D3 New Objectives, D3 additional Success Indicators added to base TSI. Roll Distance with DM–4."
}

# ------------------ Helper Functions ------------------
def roll_2d6():
    return random.randint(1,6) + random.randint(1,6)

def roll_3d6():
    return random.randint(1,6) + random.randint(1,6) + random.randint(1,6)

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

def generate_success_indicators(n=5):
    indicators = []
    paramount_assigned = False
    for _ in range(n):
        while True:
            ind = generate_success_indicator()
            if ind['level'] == "Paramount (1)":
                if not paramount_assigned:
                    paramount_assigned = True
                    break
                else:
                    continue
            else:
                break
        indicators.append(ind)
    return indicators

def generate_unique_circumstance():
    roll = roll_3d6()
    description = unique_circumstances_table.get(roll, "No special circumstance")
    return roll, description

def generate_post_mission_outcome():
    roll = roll_2d6()
    outcome = post_mission_outcome_table.get(roll, "No special outcome")
    is_branch = roll >= 10
    return roll, outcome, is_branch

# ------------------ Mission Class ------------------
class Mission:
    def __init__(self):
        self.objective_roll = None
        self.objective = None
        self.target_roll = None
        self.target = None
        self.target_dm = 0
        self.distance_roll = None
        self.distance = None
        self.zone = None
        self.world_roll = None
        self.world_type = None
        self.world_dm = 0
        self.world_desc = None
        self.total_dm = 0
        self.overall_diff = 0
        self.success_indicators = []
        self.unique_circumstance = None
        self.post_mission_outcome = None
        self.branches = []
        self.twist_reroll = False
        self.extra_indicators_added = 0

    def generate_base_mission(self):
        # Objective
        self.objective_roll = roll_2d6()
        self.objective = objectives_table.get(self.objective_roll, "Unknown Objective")
        # Target
        self.target_roll = roll_2d6()
        self.target, self.target_dm = targets_table.get(self.target_roll, ("Unknown Target",0))
        # Distance
        self.distance_roll = roll_2d6()
        self.distance, self.zone = distance_table.get(self.distance_roll, ("Unknown Distance","Unknown Zone"))
        # World
        self.world_roll = roll_2d6()
        self.world_dm, self.world_type, self.world_desc = world_table.get(self.world_roll, (0,"Unknown World",""))
        # Total DM
        self.total_dm = self.target_dm + self.world_dm
        # Overall Difficulty (example simple calculation)
        self.overall_diff = roll_2d6() + self.total_dm
        # Success Indicators
        self.success_indicators = generate_success_indicators()
        # Unique circumstance
        if self.unique_circumstance is None:
            roll, desc = generate_unique_circumstance()
            self.unique_circumstance = f"{desc}"

    def generate_post_mission(self):
        roll, outcome, is_branch = generate_post_mission_outcome()
        self.post_mission_outcome = f"{outcome}"
        if roll == 2:
            self.success_indicators = generate_success_indicators()
            self.post_mission_outcome += " → Success Indicators re-rolled due to Twist!"
        if roll in [3, 4]:
            num_extra = random.randint(1, 3)
            extra_indicators = generate_success_indicators(num_extra)
            self.success_indicators.extend(extra_indicators)
            self.post_mission_outcome += f" → Added {num_extra} extra Success Indicator(s)!"
        if is_branch:
            num_new_objectives = random.randint(1,3)
            for _ in range(num_new_objectives):
                branch = Mission()
                branch.generate_base_mission()
                # Apply DM -4 for branch distance
                branch.total_dm -= 4
                branch.overall_diff = branch.distance_roll + branch.total_dm
                # Reduce number of success indicators for branches (example 1-3)
                branch.success_indicators = generate_success_indicators(random.randint(1,3))
                self.branches.append(branch)

    def generate_text(self):
        text = f"Objective: {self.objective}\n"
        text += f"Target: {self.target}\n"
        text += f"Distance: {self.distance} [{self.zone}]\n"
        text += f"World Type: {self.world_type}, {self.world_desc}\n"
        if self.overall_diff < 4:
            text += f"Easy 4+ \n"
        elif 5 <= self.overall_diff <= 6:
            text += f"Routine 6+ \n"
        elif 7 <= self.overall_diff <= 8:
            text += f"Average 8+ \n"
        elif 9 <= self.overall_diff <= 10:
            text += f"Difficult 10+ \n"
        elif 11 <= self.overall_diff <= 12:
            text += f"Very Difficult 12+ \n"
        elif 13 <= self.overall_diff <= 14:
            text += f"Formidable 14+ \n"
        else:  # 15+
            text += f"Impossible 16+ \n"
        text += "\nSuccess Indicators:\n"
        for i, ind in enumerate(self.success_indicators, start=1):
            text += (
                f"{i}. {ind['name']}\n"
                f"   Importance: {ind['level']}\n"
                f"   Success Value: {ind['success_value']}, Failure Value: {ind['failure_value']}\n"
            )
        if self.twist_reroll:
            text += "\n(Note: All success indicators were re-rolled due to Twist outcome!)\n"

        # Mark if extra indicators were added
        if self.extra_indicators_added > 0:
            text += f"\n(Note: {self.extra_indicators_added} additional success indicator(s) added by Patron modification!)\n"

        # Unique circumstance
        if self.unique_circumstance:
            text += f"\nAdditional Information: {self.unique_circumstance}\n"
        
        if self.post_mission_outcome:
            text += f"\nPost-Mission Outcome: {self.post_mission_outcome}\n"
        for i, branch in enumerate(self.branches, start=1):
            text += f"\n--- Branch Objective {i} ---\n"
            text += branch.generate_text()
        return text

# ------------------ Example Usage ------------------
if __name__ == "__main__":
    main_mission = Mission()
    main_mission.generate_base_mission()
    main_mission.generate_post_mission()
    print(main_mission.generate_text())
