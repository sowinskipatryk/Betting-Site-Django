from django.core.management.base import BaseCommand
from royalbetsapp.models import Team

TEAMS = [
    ("Arsenal", "arsenal"),
    ("Aston Villa", 'aston'),
    ("Bournemouth", 'bournemouth'),
    ("Brentford", 'brentford'),
    ("Brighton", 'brighton'),
    ("Chelsea", 'chelsea'),
    ("Crystal Palace", 'crystal'),
    ("Everton", 'everton'),
    ("Fulham", 'fulham'),
    ("Leeds United", 'leeds'),
    ("Leicester City", 'leicester'),
    ("Liverpool", 'liverpool'),
    ("Manchester City", 'city'),
    ("Manchester United", 'united'),
    ("Newcastle United", 'newcastle'),
    ("Nottingham Forest", 'nottingham'),
    ("Southampton", 'southampton'),
    ("Tottenham Hotspur", 'spurs'),
    ("West Ham United", 'westham'),
    ("Wolves", 'wolves')
]


class Command(BaseCommand):
    help = 'Populate the database with Team model instances'

    def handle(self, *args, **options):
        my_models_data = [
            {'name': team[0], 'image': f'{team[1]}.png', 'position': pos+1} for pos, team in enumerate(TEAMS)]
        Team.objects.bulk_create([Team(**data) for data in my_models_data])
        self.stdout.write(self.style.SUCCESS('Successfully populated the database with model instances'))
