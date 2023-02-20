from django.core.management.base import BaseCommand
from royalbetsapp.models import Fixture
from royalbetsapp.tasks import draw_outcomes_and_update_data, hide_fixture_from_bets
from .fixtures_generator import fixtures_list
from django.utils import timezone


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
        fixtures = Fixture.objects.bulk_create([Fixture(**data) for data in my_models_data])
        for fixture in fixtures:
            hide_fixture_from_bets.apply_async(args=[fixture.id], eta=fixture.date)
            draw_outcomes_and_update_data.apply_async(args=[fixture.id],
                                                      eta=fixture.date + timezone.timedelta(minutes=90))
        self.stdout.write(self.style.SUCCESS('Successfully populated the database with model instances'))
