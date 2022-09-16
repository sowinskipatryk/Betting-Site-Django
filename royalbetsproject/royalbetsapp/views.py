from django.shortcuts import render, redirect
from .models import Team, Fixture
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def table(request):
    teams = Team.objects.all()
    teams_sorted = []
    for team in teams:
        teams_sorted.append(team)
    n = len(teams)
    swapped = False
    for i in range(n-1):
        for j in range(0, n-i-1):
            if teams_sorted[j].league_points < teams_sorted[j+1].league_points or (teams_sorted[j].league_points == teams_sorted[j+1].league_points and teams_sorted[j].name > teams_sorted[j+1].name):
                swapped = True
                teams_sorted[j], teams_sorted[j+1] = teams_sorted[j+1], teams_sorted[j]

        if not swapped:
            return

    for id, team in enumerate(teams_sorted):
        team.position = id + 1
        team.save()

    context = {'teams': teams_sorted}
    return render(request, 'table.html', context)


def matches(request):
    fixtures = Fixture.objects.all()

    fixtures_sorted = []
    for fx in fixtures:
        fixtures_sorted.append(fx)
    n = len(fixtures)
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
