from django.contrib import admin
from . import models


@admin.register(models.Conversation)
class ConversationAdmin(admin.ModelAdmin):

    list_display = (
        "__str__",
        "count_participants",
        "count_messages",
    )

    filter_horizontal = ("participants",)


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "created",
    )
