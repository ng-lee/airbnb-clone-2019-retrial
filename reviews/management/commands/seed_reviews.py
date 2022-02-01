import random
from django.core.management import BaseCommand
from django_seed import Seed
from reviews import models as review_models
from users import models as user_models
from rooms import models as room_models


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            type=int,
            default=1,
            help="How many reviews do you want to create?",
        )

    def handle(self, *args, **options):
        number = options.get("number")
        all_users = user_models.User.objects.all()
        all_rooms = room_models.Room.objects.all()
        seeder = Seed.seeder()
        seeder.add_entity(
            review_models.Review,
            number,
            {
                "user": lambda x: random.choice(all_users),
                "room": lambda x: random.choice(all_rooms),
            },
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} reviews created!"))
