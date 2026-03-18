from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Task, Deck, Flashcard, Event


class RegisterForm(UserCreationForm):
    pal_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Name your Pal…'})
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'pal_name']


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['text', 'priority']
        widgets = {
            'text': forms.TextInput(attrs={'placeholder': 'What needs to get done?'}),
            'priority': forms.Select(),
        }


class DeckForm(forms.ModelForm):
    class Meta:
        model = Deck
        fields = ['name', 'subject']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Deck name (e.g. Biology Chapter 3)'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Subject (e.g. Science)'}),
        }


class FlashcardForm(forms.ModelForm):
    class Meta:
        model = Flashcard
        fields = ['front', 'back']
        widgets = {
            'front': forms.TextInput(attrs={'placeholder': 'Front (Question)'}),
            'back': forms.TextInput(attrs={'placeholder': 'Back (Answer)'}),
        }


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'date', 'time', 'event_type']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Event title'}),
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'event_type': forms.Select(),
        }
