from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum
from datetime import timedelta, date
import json

from .models import UserProfile, Task, StudySession, Deck, Flashcard, Event
from .forms import RegisterForm, TaskForm, DeckForm, FlashcardForm, EventForm


# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────

def get_or_create_profile(user):
    profile, created = UserProfile.objects.get_or_create(user=user)
    return profile


def update_streak(profile):
    today = timezone.now().date()
    if profile.last_study_date is None:
        profile.streak = 1
    else:
        diff = (today - profile.last_study_date).days
        if diff == 1:
            profile.streak += 1
        elif diff > 1:
            profile.streak = 1
        # diff == 0 means same day, do nothing
    profile.last_study_date = today
    profile.save()


def log_study_session(user, minutes):
    today = timezone.now().date()
    session, created = StudySession.objects.get_or_create(
        user=user,
        date=today,
        defaults={'minutes': 0, 'sessions_count': 0}
    )
    session.minutes += minutes
    session.sessions_count += 1
    session.save()
    return session


# ─────────────────────────────────────────────
#  AUTH
# ─────────────────────────────────────────────

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create UserProfile with the pal name
            UserProfile.objects.create(
                user=user,
                pal_name=form.cleaned_data['pal_name'],
                streak=1,
                last_study_date=timezone.now().date()
            )
            login(request, user)
            messages.success(request, f'Welcome to Mypal, {user.username}! 🎉')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'mypal/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Check streak on login
            profile = get_or_create_profile(user)
            today = timezone.now().date()
            if profile.last_study_date:
                diff = (today - profile.last_study_date).days
                if diff > 1:
                    profile.streak = 0
                    profile.save()
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'mypal/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


# ─────────────────────────────────────────────
#  HOME
# ─────────────────────────────────────────────

@login_required
def home_view(request):
    profile = get_or_create_profile(request.user)
    priority_tasks = Task.objects.filter(user=request.user, is_done=False).order_by(
        # order by priority: high first
        'priority'
    )[:5]

    quotes = [
        {"quote": "The secret of getting ahead is getting started.", "author": "Mark Twain"},
        {"quote": "It always seems impossible until it's done.", "author": "Nelson Mandela"},
        {"quote": "Believe you can and you're halfway there.", "author": "Theodore Roosevelt"},
        {"quote": "The beautiful thing about learning is nobody can take it away.", "author": "B.B. King"},
        {"quote": "An investment in knowledge pays the best interest.", "author": "Benjamin Franklin"},
        {"quote": "Success is the sum of small efforts, repeated day in and day out.", "author": "Robert Collier"},
        {"quote": "You don't have to be great to start, but you have to start to be great.", "author": "Zig Ziglar"},
        {"quote": "The expert in anything was once a beginner.", "author": "Helen Hayes"},
    ]
    daily_quote = quotes[timezone.now().day % len(quotes)]

    total_study_mins = StudySession.objects.filter(
        user=request.user
    ).aggregate(total=Sum('minutes'))['total'] or 0

    tasks_done = Task.objects.filter(user=request.user, is_done=True).count()
    total_cards_reviewed = Flashcard.objects.filter(
        deck__user=request.user, is_mastered=True
    ).count()

    pal_mood, pal_mood_text = profile.get_pal_mood()

    context = {
        'profile': profile,
        'priority_tasks': priority_tasks,
        'daily_quote': daily_quote,
        'total_study_mins': total_study_mins,
        'tasks_done': tasks_done,
        'total_cards_reviewed': total_cards_reviewed,
        'pal_mood': pal_mood,
        'pal_mood_text': pal_mood_text,
        'level': profile.get_level(),
        'level_title': profile.get_level_title(),
        'xp_progress': profile.get_xp_progress(),
    }
    return render(request, 'mypal/home.html', context)


# ─────────────────────────────────────────────
#  TASKS
# ─────────────────────────────────────────────

@login_required
def tasks_view(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, '📌 Task added!')
            return redirect('tasks')
    else:
        form = TaskForm()

    todo_tasks = Task.objects.filter(user=request.user, is_done=False)
    done_tasks = Task.objects.filter(user=request.user, is_done=True)

    context = {
        'form': form,
        'todo_tasks': todo_tasks,
        'done_tasks': done_tasks,
    }
    return render(request, 'mypal/tasks.html', context)


@login_required
def toggle_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.is_done = not task.is_done
    task.save()
    if task.is_done:
        # Award XP
        profile = get_or_create_profile(request.user)
        profile.xp += 10
        profile.save()
        messages.success(request, '✅ Task completed! +10 XP')
    return redirect('tasks')


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    messages.success(request, '🗑 Task deleted.')
    return redirect('tasks')


# ─────────────────────────────────────────────
#  TIMER
# ─────────────────────────────────────────────

@login_required
def timer_view(request):
    today = timezone.now().date()
    today_session = StudySession.objects.filter(
        user=request.user, date=today
    ).first()
    sessions_today = today_session.sessions_count if today_session else 0

    context = {
        'sessions_today': sessions_today,
    }
    return render(request, 'mypal/timer.html', context)


@login_required
def complete_session(request):
    # Called via POST when a Pomodoro session finishes
    if request.method == 'POST':
        minutes = int(request.POST.get('minutes', 25))
        log_study_session(request.user, minutes)

        profile = get_or_create_profile(request.user)
        profile.xp += 20
        update_streak(profile)
        profile.save()

        messages.success(request, f'🍅 Session done! +20 XP')
    return redirect('timer')


# ─────────────────────────────────────────────
#  FLASHCARDS
# ─────────────────────────────────────────────

@login_required
def flashcards_view(request):
    decks = Deck.objects.filter(user=request.user)
    deck_form = DeckForm()
    card_form = FlashcardForm()

    context = {
        'decks': decks,
        'deck_form': deck_form,
        'card_form': card_form,
        'active_deck': None,
        'cards': [],
        'current_card': None,
        'card_index': 0,
    }
    return render(request, 'mypal/flashcards.html', context)


@login_required
def study_deck(request, deck_id):
    deck = get_object_or_404(Deck, id=deck_id, user=request.user)
    decks = Deck.objects.filter(user=request.user)
    cards = deck.cards.all()
    card_index = int(request.GET.get('card', 0))

    if card_index >= cards.count():
        card_index = 0

    current_card = cards[card_index] if cards.exists() else None

    deck_form = DeckForm()
    card_form = FlashcardForm()

    context = {
        'decks': decks,
        'deck_form': deck_form,
        'card_form': card_form,
        'active_deck': deck,
        'cards': cards,
        'current_card': current_card,
        'card_index': card_index,
        'total_cards': cards.count(),
        'next_index': card_index + 1 if card_index + 1 < cards.count() else 0,
        'mastery_percent': deck.get_mastery_percent(),
    }
    return render(request, 'mypal/flashcards.html', context)


@login_required
def add_deck(request):
    if request.method == 'POST':
        form = DeckForm(request.POST)
        if form.is_valid():
            deck = form.save(commit=False)
            deck.user = request.user
            deck.save()
            messages.success(request, '🃏 Deck created!')
            return redirect('study_deck', deck_id=deck.id)
    return redirect('flashcards')


@login_required
def edit_deck(request, deck_id):
    deck = get_object_or_404(Deck, id=deck_id, user=request.user)
    if request.method == 'POST':
        form = DeckForm(request.POST, instance=deck)
        if form.is_valid():
            form.save()
            messages.success(request, '✏️ Deck updated!')
            return redirect('study_deck', deck_id=deck.id)
    return redirect('flashcards')


@login_required
def delete_deck(request, deck_id):
    deck = get_object_or_404(Deck, id=deck_id, user=request.user)
    deck.delete()
    messages.success(request, '🗑 Deck deleted.')
    return redirect('flashcards')


@login_required
def add_card(request, deck_id):
    deck = get_object_or_404(Deck, id=deck_id, user=request.user)
    if request.method == 'POST':
        form = FlashcardForm(request.POST)
        if form.is_valid():
            card = form.save(commit=False)
            card.deck = deck
            card.save()
            messages.success(request, '🃏 Card added!')
    return redirect('study_deck', deck_id=deck_id)


@login_required
def edit_card(request, card_id):
    card = get_object_or_404(Flashcard, id=card_id, deck__user=request.user)
    if request.method == 'POST':
        form = FlashcardForm(request.POST, instance=card)
        if form.is_valid():
            form.save()
            messages.success(request, '✏️ Card updated!')
    return redirect('study_deck', deck_id=card.deck.id)


@login_required
def delete_card(request, card_id):
    card = get_object_or_404(Flashcard, id=card_id, deck__user=request.user)
    deck_id = card.deck.id
    card.delete()
    messages.success(request, '🗑 Card deleted.')
    return redirect('study_deck', deck_id=deck_id)


@login_required
def mark_card(request, card_id):
    card = get_object_or_404(Flashcard, id=card_id, deck__user=request.user)
    result = request.POST.get('result')
    next_index = int(request.POST.get('next_index', 0))

    if result == 'correct' and not card.is_mastered:
        card.is_mastered = True
        card.save()
        profile = get_or_create_profile(request.user)
        profile.xp += 5
        profile.save()
        messages.success(request, '🌟 Correct! +5 XP')
    elif result == 'wrong':
        card.is_mastered = False
        card.save()
        messages.info(request, '📖 Keep reviewing this one!')

    return redirect(f"{'/flashcards/deck/' + str(card.deck.id) + '/study/'}?card={next_index}")


# ─────────────────────────────────────────────
#  ANALYTICS
# ─────────────────────────────────────────────

@login_required
def analytics_view(request):
    profile = get_or_create_profile(request.user)
    today = timezone.now().date()

    # Weekly study data (last 7 days)
    week_data = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        session = StudySession.objects.filter(user=request.user, date=day).first()
        week_data.append({
            'label': day.strftime('%a'),
            'minutes': session.minutes if session else 0,
        })

    # Task stats
    total_tasks = Task.objects.filter(user=request.user).count()
    done_tasks = Task.objects.filter(user=request.user, is_done=True).count()
    completion_pct = round((done_tasks / total_tasks) * 100) if total_tasks else 0

    # Flashcard mastery
    total_cards = Flashcard.objects.filter(deck__user=request.user).count()
    mastered_cards = Flashcard.objects.filter(deck__user=request.user, is_mastered=True).count()
    mastery_pct = round((mastered_cards / total_cards) * 100) if total_cards else 0

    # Total study time
    total_mins = StudySession.objects.filter(
        user=request.user
    ).aggregate(total=Sum('minutes'))['total'] or 0
    total_hours = total_mins // 60
    remaining_mins = total_mins % 60

    context = {
        'profile': profile,
        'week_data': json.dumps(week_data),
        'total_tasks': total_tasks,
        'done_tasks': done_tasks,
        'remaining_tasks': total_tasks - done_tasks,
        'completion_pct': completion_pct,
        'completion_offset': round(364 - (364 * completion_pct / 100), 2),
        'total_cards': total_cards,
        'mastered_cards': mastered_cards,
        'unmastered_cards': total_cards - mastered_cards,
        'mastery_pct': mastery_pct,
        'learning_pct': 100 - mastery_pct,
        'total_hours': total_hours,
        'remaining_mins': remaining_mins,
        'level': profile.get_level(),
        'level_title': profile.get_level_title(),
    }
    return render(request, 'mypal/analytics.html', context)


# ─────────────────────────────────────────────
#  CALENDAR
# ─────────────────────────────────────────────

@login_required
def calendar_view(request):
    events = Event.objects.filter(user=request.user).order_by('date', 'time')
    form = EventForm()
    context = {
        'events': events,
        'form': form,
    }
    return render(request, 'mypal/calendar.html', context)


@login_required
def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.save()
            messages.success(request, '📅 Event added!')
    return redirect('calendar')


@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id, user=request.user)
    event.delete()
    messages.success(request, '🗑 Event deleted.')
    return redirect('calendar')