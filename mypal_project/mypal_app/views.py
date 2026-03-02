from django.shortcuts import render, redirect
from .forms import SignUpForm, HomePageForm, TaskForm, DeckForm, FlashcardForm, TimerForm, CalenderForm
from .models import SignUp, HomePage, Task, Deck, Flashcard, Timer, Calender

# SignUp

def SignUpView(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("signup")
    else:
        form = SignUpForm()
    return render(request, "signup.html", {"form": form})

# Home
    
def HomePageView(request):
    return render(request, "home.html")



def TaskView(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("task")
    else:
        form = TaskForm()       
    tasks = Task.objects.all()
    return render(request, "task.html", {"form": form, "tasks": tasks})

# Deck
    
def DeckView(request):
    if request.method == "POST":
        form = DeckForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("deck")
    else:
        form = DeckForm()
    decks = Deck.objects.all()
    return render(request, "deck.html", {"form": form, "decks": decks})

# FlasCard

def FlashCardView(request):
    if request.method == "POST":
        form = FlashcardForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("flashcard")
    else:
        form = FlashcardForm()
    flashcards = Flashcard.objects.all()
    return render(request, "flashcard.html", {"form": form, "flashcards": flashcards})

# Timer

def TimerView(request):
    if request.method == "POST":
        form = TimerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("timer")
    else:
        form = TimerForm()
    timers = Timer.objects.all()
    return render(request, "timer.html", {"form": form, "timers": timers})

# Calender

def CalenderView(request):
    if request.method == "POST":
        form = CalenderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("calender")
    else:
        form = CalenderForm()
    calenders = Calender.objects.all()
    return render(request, "calender.html", {"form": form, "calenders": calenders})
