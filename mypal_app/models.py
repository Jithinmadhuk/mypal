from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pal_name = models.CharField(max_length=50, default='Buddy')
    xp = models.IntegerField(default=0)
    streak = models.IntegerField(default=0)
    last_study_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def get_level(self):
        return (self.xp // 100) + 1

    def get_level_title(self):
        titles = ['Scholar Pup', 'Study Cadet', 'Knowledge Seeker', 'Brain Explorer', 'Wisdom Master']
        level = self.get_level()
        return titles[min(level - 1, len(titles) - 1)]

    def get_xp_progress(self):
        # XP progress within current level (0-100)
        return self.xp % 100

    def get_pal_mood(self):
        if self.xp >= 200:
            return ('excited', '🌟 On fire! Keep going!')
        elif self.xp >= 100:
            return ('excited', '😄 Amazing progress!')
        elif self.xp >= 50:
            return ('happy', '😊 Feeling good!')
        elif self.xp >= 10:
            return ('happy', '🙂 Getting started!')
        else:
            return ('sleepy', '😴 Just starting out…')


class Task(models.Model):
    PRIORITY_CHOICES = [
        ('high', 'High'),
        ('med', 'Medium'),
        ('low', 'Low'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    text = models.CharField(max_length=300)
    priority = models.CharField(max_length=4, choices=PRIORITY_CHOICES, default='med')
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-created_at']


class StudySession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='study_sessions')
    date = models.DateField()
    minutes = models.IntegerField(default=0)
    sessions_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.minutes} mins"

    class Meta:
        # One row per user per day
        unique_together = ['user', 'date']
        ordering = ['-date']


class Deck(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='decks')
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100, default='General')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_mastery_percent(self):
        total = self.cards.count()
        if total == 0:
            return 0
        mastered = self.cards.filter(is_mastered=True).count()
        return round((mastered / total) * 100)


class Flashcard(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE, related_name='cards')
    front = models.CharField(max_length=300)
    back = models.CharField(max_length=300)
    is_mastered = models.BooleanField(default=False)

    def __str__(self):
        return self.front


class Event(models.Model):
    EVENT_TYPES = [
        ('class', 'Class'),
        ('exam', 'Exam'),
        ('assignment', 'Assignment'),
        ('event', 'Event'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField(null=True, blank=True)
    event_type = models.CharField(max_length=10, choices=EVENT_TYPES, default='event')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['date', 'time']
