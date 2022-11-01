import numpy as np


def draw_results(home_odds, draw_odds, away_odds):
    goal_perc_list = [7.7, 13.8, 23.1, 24.6, 12.4, 9.3, 5.1, 2.5, 1.1, 0.3, 0.1]
    goal_prob_list = [x/100 for x in goal_perc_list]

    home_win_prob = 1/home_odds
    draw_prob = 1/draw_odds
    away_win_prob = 1/away_odds
    prob_sum = home_win_prob + draw_prob + away_win_prob

    match_result = np.random.choice([1, 0, 2], p=[home_win_prob/prob_sum, draw_prob/prob_sum, away_win_prob/prob_sum])
    match_goals = np.random.choice(np.arange(0, 11), p=goal_prob_list)

    if not match_result:
        if not match_goals:
            winner_goals = loser_goals = 0
        else:
            winner_goals = loser_goals = match_goals // 2
    else:
        if not match_goals:
            winner_goals = 1
            loser_goals = 0
        else:
            winner_goals = np.random.randint(0, match_goals) + 1
            loser_goals = match_goals - winner_goals

    if match_result == 2:
        return loser_goals, winner_goals
    return winner_goals, loser_goals
