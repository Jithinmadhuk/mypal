from django.contrib import admin
from .models import UserProfile, Task, StudySession, Deck, Flashcard, Event


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'pal_name', 'xp', 'streak', 'last_study_date']
    search_fields = ['user__username', 'pal_name']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['text', 'user', 'priority', 'is_done', 'created_at']
    list_filter = ['priority', 'is_done']
    search_fields = ['text', 'user__username']


@admin.register(StudySession)
class StudySessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'minutes', 'sessions_count']
    list_filter = ['date']
    search_fields = ['user__username']


@admin.register(Deck)
class DeckAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'subject', 'created_at']
    search_fields = ['name', 'user__username']


@admin.register(Flashcard)
class FlashcardAdmin(admin.ModelAdmin):
    list_display = ['front', 'deck', 'is_mastered']
    list_filter = ['is_mastered']
    search_fields = ['front', 'back']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'date', 'time', 'event_type']
    list_filter = ['event_type', 'date']
    search_fields = ['title', 'user__username']