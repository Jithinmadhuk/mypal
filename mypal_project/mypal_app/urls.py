from django.urls import path
from . import views

urlpatterns=[
    path("signup/", views.SignUpView, name="signup"),
    path("home/", views.HomePageView, name="home"),
    path("task/", views.TaskView, name="task"),
    path("deck/", views.DeckView, name="deck"),
    path("flashcard/", views.FlashCardView, name="flashcard"),
    path("timer/", views.TimerView, name="timer"),
    path("calender/", views.CalenderView, name="calender"),
]