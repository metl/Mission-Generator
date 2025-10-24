from utils.dice import roll_2d6
from utils.indicator_generator import generate_success_indicators
from utils.post_mission import generate_post_mission_outcome
from utils.circumstance_generator import generate_unique_circumstance
from tables.objectives import objectives_table
from tables.targets import targets_table
from tables.distances import distance_table
from tables.worlds import world_table
from tables.payout import get_payout
import random

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
        self.objective_roll = roll_2d6()
        self.objective = objectives_table.get(self.objective_roll, "Unknown Objective")

        self.target_roll = roll_2d6()
        self.target, self.target_dm = targets_table.get(self.target_roll, ("Unknown Target", 0))

        self.distance_roll = roll_2d6()
        self.distance, self.zone = distance_table.get(self.distance_roll, ("Unknown Distance", "Unknown Zone"))

        self.world_roll = roll_2d6()
        self.world_dm, self.world_type, self.world_desc = world_table.get(self.world_roll, (0, "Unknown World", ""))

        self.total_dm = self.target_dm + self.world_dm
        self.overall_diff = roll_2d6() + self.total_dm

        self.success_indicators = generate_success_indicators()

        if self.unique_circumstance is None:
            _, desc = generate_unique_circumstance()
            self.unique_circumstance = desc

    def generate_post_mission(self):
        roll, outcome, is_branch = generate_post_mission_outcome()
        self.post_mission_outcome = outcome

        if is_branch:
            num_new_objectives = random.randint(1, 3)
            for _ in range(num_new_objectives):
                branch = Mission()
                branch.generate_base_mission()
                branch.total_dm -= 4
                branch.overall_diff = branch.distance_roll + branch.total_dm
                branch.success_indicators = generate_success_indicators(random.randint(1, 3))
                self.branches.append(branch)

    def generate_text(self):
        text = f"Objective: {self.objective}\n"
        text += f"Target: {self.target}\n"
        text += f"Distance: {self.distance} [{self.zone}]\n"
        text += f"World Type: {self.world_type}, {self.world_desc}\n"

        if self.overall_diff < 4:
            text += "Overall Difficulty: Easy 4+\n"
        elif 5 <= self.overall_diff <= 6:
            text += "Overall Difficulty: Routine 6+\n"
        elif 7 <= self.overall_diff <= 10:
            text += "Overall Difficulty: Average 8+\n"
        elif 11 <= self.overall_diff <= 12:
            text += "Overall Difficulty: Difficult 10+\n"
        elif 13 <= self.overall_diff <= 14:
            text += "Overall Difficulty: Very Difficult 12+\n"
        elif 15 <= self.overall_diff <= 16:
            text += "Overall Difficulty: Formidable 14+\n"
        else:
            text += "Overall Difficulty: Impossible 16+\n"

        if self.unique_circumstance:
            text += f"\nAdditional Information: {self.unique_circumstance}\n"

        if self.post_mission_outcome:
            text += f"\nPost-Mission Outcome: {self.post_mission_outcome}\n"

        for i, branch in enumerate(self.branches, start=1):
            text += f"\n--- Branch Objective {i} ---\n"
            text += branch.generate_text()

        return text
