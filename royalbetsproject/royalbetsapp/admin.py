from django.contrib import admin
from .models import Team, Fixture, ExtendedUser


class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'league_points', 'wins', 'draws', 'losses', 'goals_scored', 'goals_conceded', 'matches_played', 'form')


class FixtureAdmin(admin.ModelAdmin):
    list_display = ('team_home', 'team_away', 'week', 'date')


admin.site.register(Team, TeamAdmin)
admin.site.register(Fixture, FixtureAdmin)
admin.site.register(ExtendedUser)
