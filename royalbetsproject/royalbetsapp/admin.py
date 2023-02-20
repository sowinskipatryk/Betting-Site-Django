from django.contrib import admin
from .models import Team, Fixture, ExtendedUser, Coupon, Bet


class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'league_points', 'wins', 'draws', 'losses', 'goals_scored', 'goals_conceded', 'matches_played', 'form')


class FixtureAdmin(admin.ModelAdmin):
    list_display = ('team_home', 'team_away', 'week', 'date')


class CouponAdmin(admin.ModelAdmin):
    list_display = ('coupon_id', 'creator', 'type', 'stake', 'odds', 'prize', 'outcome', 'create_date')


class ExtendedUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance', 'points')


class BetAdmin(admin.ModelAdmin):
    list_display = ('pick', 'fixture', 'outcome', 'coupon')


admin.site.register(Team, TeamAdmin)
admin.site.register(Fixture, FixtureAdmin)
admin.site.register(ExtendedUser, ExtendedUserAdmin)
admin.site.register(Coupon, CouponAdmin)
admin.site.register(Bet, BetAdmin)
