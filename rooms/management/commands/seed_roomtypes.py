from django.core.management import BaseCommand
from rooms import models as room_models


class Command(BaseCommand):
    def handle(self, *args, **options):
        room_types = [
            "Entire place",
            "Private rooms",
            "Hotel rooms",
            "Shared rooms",
        ]
        for t in room_types:
            room_models.RoomType.objects.create(name=t)
        self.stdout.write(self.style.SUCCESS(f"{len(room_types)} room types created!"))
