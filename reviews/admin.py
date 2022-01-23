from django.contrib import admin
from . import models


@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):

    fieldsets = (
        (
            "Basic Info",
            {
                "fields": (
                    "user",
                    "room",
                    "review",
                )
            },
        ),
        (
            "Ratings",
            {
                "fields": (
                    "accuracy",
                    "communication",
                    "cleanliness",
                    "location",
                    "check_in",
                    "value",
                )
            },
        ),
    )

    list_display = (
        "user",
        "room",
        "average_rating",
    )
