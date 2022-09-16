from itertools import permutations
from datetime import datetime, timedelta
import random

match_dict = dict()
match_list = []

match_id = 0

teams = [x for x in range(1, 21)]
matches = permutations(teams, 2)

match_dates = []
gap_week = 1
week = 1
dt = datetime(2022, 8, 1)
dt += timedelta(days=4 - dt.weekday())
while dt < datetime(2023, 6, 1):
    if gap_week % 8:
        match_dates.append((week, dt, dt + timedelta(days=1), dt + timedelta(days=2)))
        week += 1
    gap_week += 1
    dt += timedelta(days=7)

for match in matches:
    for meet in range(2):
        if meet % 2:
            match_dict['team_home'] = match[0]
            match_dict['team_away'] = match[1]
        else:
            match_dict['team_home'] = match[1]
            match_dict['team_away'] = match[0]
        perc_home = random.randint(20, 60)
        perc_draw = random.randint(20, min(40, 100 - perc_home))
        perc_away = 105 - perc_home - perc_draw
        odd_home = round(105 / perc_home, 2)
        odd_draw = round(105 / perc_draw, 2)
        odd_away = round(105 / perc_away, 2)
        match_dict['odds_team_home'] = '%.2f' % odd_home
        match_dict['odds_draw'] = '%.2f' % odd_draw
        match_dict['odds_team_away'] = '%.2f' % odd_away
        match_id += 1
        match_dict['match_num'] = match_id
        draw_date = random.choice(match_dates)
        match_dict['week'] = draw_date[0]
        match_dict['date'] = draw_date[random.randint(1, 3)] + timedelta(hours=random.choice(range(12, 21)), minutes=random.choice([0, 15, 30, 45]))
        match_list.append((tuple(match_dict.values())))

random.shuffle(match_list)

# for m in match_list:
#     print(m)
