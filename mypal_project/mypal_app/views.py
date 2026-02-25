from django.shortcuts import render, redirect
from .forms import SignUpForm, HomePageForm, TaskForm, DeckForm, FlashcardForm, TimerForm, CalenderForm
from .models import SignUp, HomePage, Task, Deck, Flashcard, Timer, Calender

def SignUpView(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home_page')
        else:
            form = SignUpForm()
        return render(request, 'signup_page.html', {'form': form})

