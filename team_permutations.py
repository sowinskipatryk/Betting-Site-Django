from itertools import permutations
from datetime import date, timedelta
import random

# match_dates = []
# dt = date(2022, 8, 1)
# dt += timedelta(days=4 - dt.weekday())
# while dt < date(2023, 6, 1):
#     match_dates.append(dt)
#     match_dates.append(dt + timedelta(days=1))
#     match_dates.append(dt + timedelta(days=2))
#     dt += timedelta(days=7)
#
# teams = [i for i in range(20)]
#
# matches = permutations(teams, 2)
# matches_list = []
#
# for match in matches:
#     print(match[0])
#     print(match[1])
#     matches_list.append((match, random.choice(match_dates)))
#
# print(matches_list)

perc_home = random.randint(20, 60)
perc_draw = random.randint(20, min(40, 100 - perc_home))
perc_away = 105 - perc_home - perc_draw
odd_home = round(105 / perc_home, 2)
odd_draw = round(105 / perc_draw, 2)
odd_away = round(105 / perc_away, 2)

print(odd_home, odd_draw, odd_away)
