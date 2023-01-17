import random

ODD_BASE = 105


def generate_odds():
    perc_home = random.randint(20, 60)
    perc_draw = random.randint(20, min(40, 100 - perc_home))
    perc_away = ODD_BASE - perc_home - perc_draw
    odd_home = round(ODD_BASE / perc_home, 2)
    odd_draw = round(ODD_BASE / perc_draw, 2)
    odd_away = round(ODD_BASE / perc_away, 2)
    return odd_home, odd_draw, odd_away
