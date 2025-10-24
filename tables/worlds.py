import random
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