from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Team, Fixture, Coupon, ExtendedUser, Bet, COUPON_TYPES
from .forms import RegisterForm
import json
import random


def table(request):
    teams = Team.objects.all().order_by('-league_points', '-wins', '-goals_scored', 'goals_conceded', 'name')
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
        print(user)
        if user:
            print('if user')
            if user.is_active:
                print('if active')
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
    coupons = Coupon.objects.filter(creator=request.user).order_by('-create_date')
    coupon_data = []
    for coupon in coupons:
        bet_data = []
        bets = Bet.objects.filter(coupon=coupon)
        for bet in bets:
            bet_data.append({'fixture': bet.fixture, 'pick': bet.pick, 'outcome': bet.outcome})
        coupon_data.append({'coupon_details': coupon, 'bets_details': bet_data})
    context = {'coupons': coupon_data, 'types': COUPON_TYPES}
    return render(request, 'coupons.html', context)


def leaderboard(request):
    users = ExtendedUser.objects.all().order_by('-overall')
    context = {'users': users}
    return render(request, 'leaderboard.html', context)
