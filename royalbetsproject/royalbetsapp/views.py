from datetime import datetime
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Team, Fixture, Coupon, ExtendedUser, User, Bet
from .forms import RegisterForm
from .utils import draw_results
import json
import random


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


def odds(request):
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
        matches = paginator.page(page)
    except PageNotAnInteger:
        matches = paginator.page(1)
    except EmptyPage:
        matches = paginator.page(paginator.num_pages)
    context = {'matches': matches}
    return render(request, 'odds.html', context)


def index(request):
    return redirect('/odds')


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
        matches = paginator.page(page)
    except PageNotAnInteger:
        matches = paginator.page(1)
    except EmptyPage:
        matches = paginator.page(paginator.num_pages)
    context = {'matches': matches}
    return render(request, 'results.html', context)


@login_required
def coupon_submit(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        coupon_id = random.randint(10**15, (10**16)-1)
        bets = data["betsInput"]

        if len(bets) == 1:
            betType = 0
        else:
            betType = 1

        stake = float(data["stakeInput"])
        odds = float(data["oddsInput"])
        prize = float(data["prizeInput"][1:])

        if request.user.is_authenticated:
            creator = User.objects.get(username=request.user.username)
            coupon = Coupon(coupon_id=coupon_id, type=betType,
                        creator=creator, stake=stake, odds=odds, prize=prize)

            coupon.save()

            for bet in bets:
                new_bet = Bet(coupon=coupon, fixture=Fixture.objects.get(id=bet['matchId']), pick=bet['matchPick'])
                new_bet.save()

        return JsonResponse({"status": "success"})


def register_view(request):
    registered = False
    if request.method == "POST":
        register_form = RegisterForm(data=request.POST)

        if register_form.is_valid():
            user = register_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
            login(request, user)
            return HttpResponseRedirect(reverse('odds'))
        else:
            HttpResponseRedirect('Registration failed!')
    else:
        register_form = RegisterForm()
        for field in register_form.fields:
            register_form[field].help_text = ''

    return render(request, 'register.html', {'register_form': register_form,
                                             'registered': registered})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponseRedirect('Account is blocked, deleted or inactive!')
        else:
            return HttpResponseRedirect('Invalid login credentials!')
    else:
        return render(request, 'login.html')


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('odds'))


@login_required
def coupon_history(request):
    coupons = Coupon.objects.all()
    context = {'coupons': coupons}
    return render(request, 'coupons.html', context)
