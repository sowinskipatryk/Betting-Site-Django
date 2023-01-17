import random
from datetime import datetime, timedelta
from .odds_generator import generate_odds

teams = [i for i in range(1, 21)]
teams_num = len(teams)
weeks_num = (len(teams)-1) * 2
matches_num = teams_num // 2
match_id = 1

up = 2
down = teams_num

fixtures_list = []
gap_week = 0
dt = datetime(2022, 8, 1)
dt += timedelta(days=4 - dt.weekday())
for week in range(1, weeks_num+1):
    match_dates = [dt, dt + timedelta(days=1), dt + timedelta(days=2)]
    home = up
    away = down
    for match in range(matches_num):
        fixture = {}
        if match == 0:
            if week > weeks_num // 2:
                fixture['team_away_id'] = 1
            else:
                fixture['team_home_id'] = 1
        else:
            if week > weeks_num // 2:
                fixture['team_away_id'] = home
            else:
                fixture['team_home_id'] = home
            home += 1
        if week > weeks_num // 2:
            fixture['team_home_id'] = away
        else:
            fixture['team_away_id'] = away
        away -= 1

        if home > teams_num:
            home = 2
        if away == 1:
            away = teams_num

        fixture['week'] = week
        fixture['match_num'] = match_id

        odd_home, odd_draw, odd_away = generate_odds()
        fixture['odds_team_home'] = '%.2f' % odd_home
        fixture['odds_draw'] = '%.2f' % odd_draw
        fixture['odds_team_away'] = '%.2f' % odd_away

        match_date = random.choice(match_dates)
        fixture['date'] = match_date + timedelta(
            hours=random.choice(range(12, 21)),
            minutes=random.choice([0, 15, 30, 45]))
        fixtures_list.append(fixture)
        match_id += 1

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
