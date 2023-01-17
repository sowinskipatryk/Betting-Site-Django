from datetime import datetime, timedelta
import random

teams = [i for i in range(1, 21)]
teams_num = len(teams)
weeks_num = (len(teams)-1) * 1
matches_num = teams_num // 2
match_num = 1

up = 2
down = teams_num

match_list = []
weeks_dict = {}
week_list = []
gap_week = 0
dt = datetime(2022, 8, 1)
dt += timedelta(days=4 - dt.weekday())
for week in range(1, weeks_num):
    match_dates = [dt, dt + timedelta(days=1), dt + timedelta(days=2)]
    home = up
    away = down
    for match in range(matches_num):
        match_dict = {}
        if match == 0:
            week_list.append((1, away))
            match_dict['team_home'] = 1
        else:
            week_list.append((home, away))
            match_dict['team_home'] = home
            home += 1
        match_dict['team_away'] = away
        away -= 1

        if home > teams_num:
            home = 2
        if away == 1:
            away = teams_num

        match_dict['week'] = week
        match_dict['match_num'] = match_num

        perc_home = random.randint(20, 60)
        perc_draw = random.randint(20, min(40, 100 - perc_home))
        perc_away = 105 - perc_home - perc_draw
        odd_home = round(105 / perc_home, 2)
        odd_draw = round(105 / perc_draw, 2)
        odd_away = round(105 / perc_away, 2)
        match_dict['odds_team_home'] = '%.2f' % odd_home
        match_dict['odds_draw'] = '%.2f' % odd_draw
        match_dict['odds_team_away'] = '%.2f' % odd_away

        match_date = random.choice(match_dates)
        match_dict['date'] = match_date + timedelta(
            hours=random.choice(range(12, 21)),
            minutes=random.choice([0, 15, 30, 45]))
        # print(match_dict)
        match_dict['played'] = False
        match_dict['result_home'] = 0
        match_dict['result_away'] = 0
        match_dict['winner_home'] = False
        match_dict['winner_away'] = False
        match_dict['table_updated'] = False
        match_list.append((tuple(match_dict.values())))
        match_num += 1

    weeks_dict[week] = week_list

    up -= 1
    if up == 1:
        up = teams_num
    down -= 1
    if down == 1:
        down = teams_num

    gap_week += 1
    dt += timedelta(days=7)
    if gap_week % 8:
        dt += timedelta(days=7)
        gap_week = 0

# print(weeks_dict)

print(match_list)
