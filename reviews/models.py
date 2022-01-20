from django.db import models
from core import models as core_models


class Review(core_models.TimeStampedModel):

    """Review Model Definition"""

    RATING_ONE = 1
    RATING_TWO = 2
    RATING_THREE = 3
    RATING_FOUR = 4
    RATING_FIVE = 5
    RATING_CHOICE = (
        (RATING_ONE, "1"),
        (RATING_TWO, "2"),
        (RATING_THREE, "3"),
        (RATING_FOUR, "4"),
        (RATING_FIVE, "5"),
    )

    review = models.TextField()
    accuracy = models.IntegerField(choices=RATING_CHOICE)
    communication = models.IntegerField(choices=RATING_CHOICE)
    cleanliness = models.IntegerField(choices=RATING_CHOICE)
    location = models.IntegerField(choices=RATING_CHOICE)
    check_in = models.IntegerField(choices=RATING_CHOICE)
    value = models.IntegerField(choices=RATING_CHOICE)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    room = models.ForeignKey("rooms.Room", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user}: {self.room}"
