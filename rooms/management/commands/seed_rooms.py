import random
from django.core.management import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from rooms import models as room_models
from users import models as user_models


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            type=int,
            default=1,
            help="How many rooms do you want to create?",
        )

    def handle(self, *args, **options):
        number = options.get("number")
        all_users = user_models.User.objects.all()
        room_types = room_models.RoomType.objects.all()
        seeder = Seed.seeder()
        seeder.add_entity(
            room_models.Room,
            number,
            {
                "name": lambda x: seeder.faker.address(),
                "host": lambda x: random.choice(all_users),
                "room_type": lambda x: random.choice(room_types),
                "price": lambda x: random.randint(0, 300),
                "guests": lambda x: random.randint(0, 20),
                "beds": lambda x: random.randint(0, 5),
                "bedrooms": lambda x: random.randint(0, 5),
                "baths": lambda x: random.randint(0, 5),
            },
        )
        created = seeder.execute()
        cleaned = flatten(list(created.values()))
        all_amenities = room_models.Amenity.objects.all()
        all_facilities = room_models.Facility.objects.all()
        all_house_rules = room_models.HouseRule.objects.all()
        for pk in cleaned:
            room = room_models.Room.objects.get(pk=pk)
            for _ in range(random.randint(5, 15)):
                room_models.Photo.objects.create(
                    caption=seeder.faker.sentence(),
                    file=f"room_photos/{random.randint(0, 31)}.webp",
                    room=room,
                )
            for amenity in all_amenities:
                trigger = random.randint(0, 10)
                if trigger % 2:
                    room.amenities.add(amenity)
            for facility in all_facilities:
                trigger = random.randint(0, 10)
                if trigger % 2:
                    room.facilities.add(facility)
            for rule in all_house_rules:
                trigger = random.randint(0, 10)
                if trigger % 2:
                    room.house_rules.add(rule)
        self.stdout.write(self.style.SUCCESS(f"{number} rooms created!"))
