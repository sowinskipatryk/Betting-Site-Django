from celery import shared_task
from .models import Team, ExtendedUser, Bet, Fixture
from .utils import draw_results


@shared_task
def hide_fixture_from_bets(id):
    fx = Fixture.objects.get(id=id)
    fx.played = True
    fx.save()


@shared_task
def draw_outcomes_and_update_data(id):
    fx = Fixture.objects.get(id=id)
    fx.result_home, fx.result_away = draw_results(fx.odds_team_home, fx.odds_draw, fx.odds_team_away)
    fx.save()
    fx.update_teams_data()

    teams = Team.objects.all().order_by('-league_points', '-wins', '-goals_scored', 'goals_conceded', 'name')
    for id, tm in enumerate(teams):
        tm.position = id + 1
        tm.save()

    bets = Bet.objects.filter(fixture=fx)
    for bet in bets:
        if (fx.winner_home and bet.pick == '1') or (
                fx.winner_away and bet.pick == '2') or (
                not fx.winner_home and not fx.winner_away and bet.pick == 'X'):
            bet.outcome = 1
            bet.save()
            coupon_bets = Bet.objects.filter(coupon=bet.coupon)
            if all(cpbet.outcome == 1 for cpbet in coupon_bets):
                bet.coupon.outcome = 1
                bet.coupon.save()
                ext_user = ExtendedUser.objects.get(user=bet.coupon.creator)
                ext_user.balance += bet.coupon.prize
                ext_user.points += int((bet.coupon.prize - bet.coupon.stake) * 100)
                ext_user.save()

        else:
            bet.outcome = 2
            bet.save()
            if bet.coupon.outcome != 2:
                bet.coupon.outcome = 2
                bet.coupon.prize = 0
                bet.coupon.save()
                ext_user = ExtendedUser.objects.get(user=bet.coupon.creator)
                ext_user.points -= int(bet.coupon.stake * 100)
                ext_user.save()
