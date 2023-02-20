from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Team(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(null=True, blank=True, upload_to='')
    position = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    league_points = models.IntegerField(default=0)
    goals_scored = models.IntegerField(default=0)
    goals_conceded = models.IntegerField(default=0)
    matches_played = models.IntegerField(default=0)
    form = models.CharField(max_length=5, default='?????')

    def __str__(self):
        return self.name

    @property
    def image_url(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    def clear_data(self):
        self.matches_played = 0
        self.wins = 0
        self.draws = 0
        self.losses = 0
        self.league_points = 0
        self.form = '?????'
        self.goals_scored = 0
        self.goals_conceded = 0
        self.save()


class Fixture(models.Model):
    team_home = models.ForeignKey(Team, on_delete=models.SET_NULL, related_name='home_team', null=True)
    team_away = models.ForeignKey(Team, on_delete=models.SET_NULL, related_name='away_team', null=True)
    odds_team_home = models.DecimalField(max_digits=4, decimal_places=2)
    odds_draw = models.DecimalField(max_digits=4, decimal_places=2)
    odds_team_away = models.DecimalField(max_digits=4, decimal_places=2)
    match_num = models.IntegerField(default=0)
    week = models.IntegerField(default=0)
    date = models.DateTimeField()
    played = models.BooleanField(default=False)
    result_home = models.IntegerField(default=None, null=True, blank=True)
    result_away = models.IntegerField(default=None, null=True, blank=True)
    winner_home = models.BooleanField(default=False)
    winner_away = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.team_home} - {self.team_away}"

    def update_teams_data(self):
        if self.result_home > self.result_away:
            self.winner_home = True
            self.winner_away = False
        elif self.result_home < self.result_away:
            self.winner_away = True
            self.winner_home = False
        else:
            self.winner_home = False
            self.winner_away = False

        self.team_home.matches_played += 1
        self.team_away.matches_played += 1

        if self.winner_home:
            self.team_home.league_points += 3
            self.team_home.wins += 1
            self.team_away.losses += 1
            self.team_home.form = 'W' + self.team_home.form[:4]
            self.team_away.form = 'L' + self.team_away.form[:4]

        elif self.winner_away:
            self.team_away.league_points += 3
            self.team_away.wins += 1
            self.team_home.losses += 1
            self.team_home.form = 'L' + self.team_home.form[:4]
            self.team_away.form = 'W' + self.team_away.form[:4]

        else:
            self.team_home.league_points += 1
            self.team_away.league_points += 1
            self.team_home.draws += 1
            self.team_away.draws += 1
            self.team_home.form = 'D' + self.team_home.form[:4]
            self.team_away.form = 'D' + self.team_away.form[:4]

        self.team_home.goals_scored += self.result_home
        self.team_away.goals_scored += self.result_away
        self.team_home.goals_conceded += self.result_away
        self.team_away.goals_conceded += self.result_home

        self.save()
        self.team_home.save()
        self.team_away.save()


COUPON_TYPES = [
    (0, 'Single'),
    (1, 'Multi'),
]

COUPON_OUTCOMES = [
    (0, 'Open'),
    (1, 'Won'),
    (2, 'Lost'),
]

MATCH_PICKS = [
    ('1', 'Home'),
    ('X', 'Draw'),
    ('2', 'Away'),
]


class Coupon(models.Model):
    coupon_id = models.IntegerField(primary_key=True)
    type = models.IntegerField(choices=COUPON_TYPES)
    create_date = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    stake = models.FloatField()
    odds = models.FloatField()
    outcome = models.IntegerField(choices=COUPON_OUTCOMES, default=0)
    prize = models.FloatField()

    def __str__(self):
        return str(self.coupon_id)


class Bet(models.Model):
    fixture = models.ForeignKey(Fixture, on_delete=models.CASCADE)
    pick = models.CharField(choices=MATCH_PICKS, max_length=4)
    outcome = models.IntegerField(choices=COUPON_OUTCOMES, default=0)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, default=None, null=True)

    def __str__(self):
        return f"{self.fixture} Pick: {self.pick}"


class ExtendedUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.FloatField(default=0.00)
    avatar = models.ImageField(upload_to='profile_pics', null=True, blank=True)
    coupons = models.ManyToManyField(Coupon, blank=True)
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_custom_user(sender, instance, created, **kwargs):
    if created:
        ExtendedUser.objects.create(user=instance, balance=100.)
