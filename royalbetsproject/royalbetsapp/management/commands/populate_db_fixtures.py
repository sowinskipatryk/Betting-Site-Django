from django.core.management.base import BaseCommand
from royalbetsapp.models import Fixture
from .fixtures_generator import fixtures_list


class Command(BaseCommand):
    help = 'Populate the database with Fixture model instances'

    def handle(self, *args, **options):
        my_models_data = [
            {'team_home_id': fixture['team_home_id'],
             'team_away_id': fixture['team_away_id'],
             'odds_team_home': fixture['odds_team_home'],
             'odds_draw': fixture['odds_draw'],
             'odds_team_away': fixture['odds_team_away'],
             'match_num': fixture['match_num'],
             'week': fixture['week'],
             'date': fixture['date']} for fixture in fixtures_list]
        Fixture.objects.bulk_create([Fixture(**data) for data in my_models_data])
        self.stdout.write(self.style.SUCCESS('Successfully populated the database with model instances'))
