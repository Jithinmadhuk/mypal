from django import forms
from .models import SignUp, HomePage, Task, Deck, Flashcard, Timer, Calender

class SignUpForm(forms.ModelForm):
    class Meta:
        model = SignUp
        fields = ['first_name','middle_name','last_name','email','password']

class HomePageForm(forms.ModelForm):
    class Meta:
        model = HomePage
        fields = ['user','pal','streaks','last_study_date','xp']

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['user','title','priority','description','is_done']

class DeckForm(forms.ModelForm):
    class Meta:
        model = Deck
        fields = ['user','subject','chapter']

class FlashcardForm(forms.ModelForm):
    class Meta:
        model = Flashcard
        fields = ['user','question','answer']

class TimerForm(forms.ModelForm):
    class Meta:
        model = Timer
        fields = ['user','date','minutes','sessions']

class CalenderForm(forms.ModelForm):
    class Meta:
        model = Calender
        fields = ['user','title','type','date','time']

