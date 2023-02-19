import random
from datetime import datetime, timedelta
from .odds_generator import generate_odds
from django.utils import timezone

teams = [i for i in range(1, 21)]
teams_num = len(teams)
weeks_num = (len(teams)-1) * 2
matches_num = teams_num // 2
match_id = 1

up = 2
down = teams_num

fixtures_list = []

dt = datetime.now()
for week in range(1, weeks_num+1):
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

        h, m = random.choice([(13, 30), (14, 30), (15, 0),  (15, 30), (16, 0), (17, 30), (18, 30), (20, 45), (21, 0)])
        tz = timezone.get_current_timezone()
        match_date = timezone.make_aware(dt.replace(hour=h, minute=m, second=0, microsecond=0), tz)
        fixture['date'] = match_date
        fixtures_list.append(fixture)
        match_id += 1

    up -= 1
    if up == 1:
        up = teams_num
    down -= 1
    if down == 1:
        down = teams_num

    dt += timedelta(days=1)
