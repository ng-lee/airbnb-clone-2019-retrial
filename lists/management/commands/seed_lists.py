import random
from django.core.management import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from lists import models as list_models
from users import models as user_models
from rooms import models as room_models


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            type=int,
            default=1,
            help="How many lists do you want to create?",
        )

    def handle(self, *args, **options):
        number = options.get("number")
        all_users = user_models.User.objects.all()
        seeder = Seed.seeder()
        seeder.add_entity(
            list_models.List, number, {"user": lambda x: random.choice(all_users)}
        )
        created = seeder.execute()
        cleaned = flatten(list(created.values()))
        all_rooms = room_models.Room.objects.all()
        for pk in cleaned:
            list_model = list_models.List.objects.get(pk=pk)
            for room in all_rooms:
                trigger = random.randint(0, 10)
                if trigger % 3 == 0:
                    list_model.rooms.add(room)
        self.stdout.write(self.style.SUCCESS(f"{number} lists created!"))
