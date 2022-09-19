from datetime import datetime
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Team, Fixture
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


def table(request):
    teams = Team.objects.all()
    # for tm in teams:
    #     tm.clear_data()

    fixtures = Fixture.objects.all()
    for fx in fixtures:
        # fx.table_updated = False
        # fx.save()
        if fx.played and not fx.table_updated:
            fx.update_table()

    teams_sorted = []
    for tm in teams:
        teams_sorted.append(tm)
    n = len(teams)
    for i in range(n-1):
        for j in range(0, n-i-1):
            if teams_sorted[j].league_points < teams_sorted[j+1].league_points or (teams_sorted[j].league_points == teams_sorted[j+1].league_points and teams_sorted[j].name > teams_sorted[j+1].name):
                teams_sorted[j], teams_sorted[j+1] = teams_sorted[j+1], teams_sorted[j]

    for id, tm in enumerate(teams_sorted):
        tm.position = id + 1
        tm.save()

    context = {'teams': teams_sorted}
    return render(request, 'table.html', context)


def matches(request):
    fixtures = Fixture.objects.all()

    fixtures_sorted = []
    for fx in fixtures:
        if not fx.played:
            fixtures_sorted.append(fx)
    n = len(fixtures_sorted)
    for i in range(n-1):
        for j in range(0, n-i-1):
            if fixtures_sorted and fixtures_sorted[j].date > fixtures_sorted[j+1].date:
                fixtures_sorted[j], fixtures_sorted[j+1] = fixtures_sorted[j+1], fixtures_sorted[j]

    page = request.GET.get('page', 1)
    paginator = Paginator(fixtures_sorted, 10)
    try:
        matches_page = paginator.page(page)
    except PageNotAnInteger:
        matches_page = paginator.page(1)
    except EmptyPage:
        matches_page = paginator.page(paginator.num_pages)
    context = {'matches': matches_page}
    return render(request, 'matches.html', context)


def index(request):
    return redirect('/matches')


def results(request):
    fixtures = Fixture.objects.all()

    fixtures_sorted = []
    for fx in fixtures:
        if fx.date.timestamp() < datetime.now().timestamp() and not fx.played:
            fx.played = True
            fx.result_home, fx.result_away = draw_results(fx.odds_team_home, fx.odds_draw, fx.odds_team_away)

            if fx.result_home > fx.result_away:
                fx.winner_home = True
                fx.winner_away = False
            elif fx.result_home < fx.result_away:
                fx.winner_away = True
                fx.winner_home = False
            else:
                fx.winner_home = False
                fx.winner_away = False

            fx.save()

        if fx.played:
            fixtures_sorted.append(fx)
    n = len(fixtures_sorted)

    for i in range(n-1):
        for j in range(0, n-i-1):
            if fixtures_sorted[j].date < fixtures_sorted[j+1].date:
                fixtures_sorted[j], fixtures_sorted[j+1] = fixtures_sorted[j+1], fixtures_sorted[j]

    page = request.GET.get('page', 1)
    paginator = Paginator(fixtures_sorted, 20)
    try:
        matches_page = paginator.page(page)
    except PageNotAnInteger:
        matches_page = paginator.page(1)
    except EmptyPage:
        matches_page = paginator.page(paginator.num_pages)
    context = {'matches': matches_page}
    return render(request, 'results.html', context)
