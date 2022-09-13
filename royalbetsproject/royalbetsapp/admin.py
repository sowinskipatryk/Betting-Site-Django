from django.contrib import admin
from .models import Team, Fixture


class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'league_points', 'wins', 'draws', 'losses', 'goals_scored', 'goals_conceded', 'matches_played', 'form')


admin.site.register(Team, TeamAdmin)
admin.site.register(Fixture)
