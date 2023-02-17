from datetime import datetime
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Team, Fixture, Coupon, ExtendedUser, Bet, COUPON_TYPES
from .forms import RegisterForm
from .utils import draw_results
import json
import random


def table(request):
    teams = Team.objects.all().order_by('-league_points', '-wins', '-goals_scored', 'goals_conceded', 'name')
    for id, tm in enumerate(teams):
        tm.position = id + 1
        tm.save()

    context = {'teams': teams}
    return render(request, 'table.html', context)


def odds(request):
    fixtures = Fixture.objects.filter(played=False).order_by('date')

    page = request.GET.get('page', 1)
    paginator = Paginator(fixtures, 10)
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
    fixtures_notplayed = Fixture.objects.filter(played=False)

    for fx in fixtures_notplayed:
        if fx.date.timestamp() < datetime.now().timestamp():
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

            fx.update_table()
            fx.save()

    fixtures_played = Fixture.objects.filter(played=True).order_by('-date')

    page = request.GET.get('page', 1)
    paginator = Paginator(fixtures_played, 20)
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
        if request.user.is_authenticated:

            data = json.loads(request.body)

            stake = float(data["stakeInput"])
            odds = float(data["oddsInput"])
            prize = float(data["prizeInput"][1:])

            creator = ExtendedUser.objects.get(user=request.user)

            if creator.balance < stake:
                return JsonResponse(
                    {"status": "error", "message": "Insufficient funds!"})

            if stake > 500_000:
                return JsonResponse(
                    {"status": "error", "message": "Maximum prize exceeded!"})

            coupon_id = random.randint(10 ** 15, (10 ** 16) - 1)

            bets = data["betsInput"]
            if len(bets) == 1:
                betType = 0
            else:
                betType = 1

            coupon = Coupon(coupon_id=coupon_id, type=betType,
                        creator=creator.user, stake=stake, odds=odds, prize=prize)

            coupon.save()

            creator.balance -= stake
            creator.save()

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

    open_coupons = Coupon.objects.filter(creator=request.user, outcome=0)
    for coup in open_coupons:
        open_bets = Bet.objects.filter(coupon=coup)
        bet_outcomes = []
        for bet in open_bets:
            if bet.fixture.played:
                if (bet.fixture.winner_home and bet.pick == '1') or (
                        bet.fixture.winner_away and bet.pick == '2') or (
                        not bet.fixture.winner_home and not bet.fixture.winner_away and bet.pick == 'X'):
                    bet.outcome = 1
                else:
                    bet.outcome = 2
                bet.save()
                bet_outcomes.append(bet.outcome)

        if 2 in bet_outcomes:
            coup.outcome = 2
        elif bet_outcomes and not 0 in bet_outcomes:
            coup.outcome = 1
        coup.save()

    coupons = Coupon.objects.filter(creator=request.user).order_by('-create_date')
    context = {'coupons': coupons, 'types': COUPON_TYPES}
    return render(request, 'coupons.html', context)
