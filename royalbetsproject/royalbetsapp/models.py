from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(null=True, blank=True)
    position = models.IntegerField(default=0)
    wins = models.IntegerField(default=0, null=True, blank=True)
    draws = models.IntegerField(default=0, null=True, blank=True)
    losses = models.IntegerField(default=0, null=True, blank=True)
    league_points = models.IntegerField(default=0, null=True, blank=True)
    goals_scored = models.IntegerField(default=0, null=True, blank=True)
    goals_conceded = models.IntegerField(default=0, null=True, blank=True)
    matches_played = models.IntegerField(default=0, null=True, blank=True)
    form = models.CharField(max_length=5, default='?????', blank=True)

    def __str__(self):
        return self.name

    @property
    def image_url(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    @property
    def form_five_matches(self):
        while len(self.form) < 5:
            self.form += '?'
        return self.form


class Fixture(models.Model):
    team_home = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='home_team')
    team_away = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='away_team')
    odds_team_home = models.DecimalField(max_digits=4, decimal_places=2)
    odds_draw = models.DecimalField(max_digits=4, decimal_places=2)
    odds_team_away = models.DecimalField(max_digits=4, decimal_places=2)
    match_num = models.IntegerField(default=0, null=True, blank=True)
    week = models.IntegerField(default=0, null=True, blank=True)
    date = models.DateTimeField()
