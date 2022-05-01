import random
from enum import Enum

CHANCES = [50, 25, 15, 6, 4]


class Rarity(Enum):
    COMMON = 0
    UNCOMMON = 1
    RARE = 2
    MYTHIC = 3
    LEGENDARY = 4


def get_rarity(pack):
    max_rarity = len(Rarity) - 1
    for i in range(len(Rarity)):
        if len(pack[Rarity(max_rarity).name.lower()]) <= 0:
            max_rarity -= 1
    r = random.randint(0, sum(CHANCES[:max_rarity + 1]))
    for rarity in range(max_rarity + 1):
        if r <= sum(CHANCES[0:rarity + 1]):
            return rarity
    return len(CHANCES) - 1


def get_card(pack):
    r = random.randint(0, len(pack) - 1)
    return pack[r]


def choose_by_rarity(pack: dict):
    """
    Dict form
        {
            common:[],
            uncommon:[],
            rare:[],
            mythic:[],
            legendary:[]
        }
    """
    rarity = get_rarity(pack)
    name = Rarity(rarity).name.lower()
    card = get_card(pack[name])
    return card


if __name__ == "__main__":
    print(choose_by_rarity({
        "common": [1],
        "uncommon": [2],
        "rare": [],
        "mythic": [],
        "legendary": []
    }))
