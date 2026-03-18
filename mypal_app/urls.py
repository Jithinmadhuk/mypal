from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Home
    path('', views.home_view, name='home'),

    # Tasks
    path('tasks/', views.tasks_view, name='tasks'),
    path('tasks/toggle/<int:task_id>/', views.toggle_task, name='toggle_task'),
    path('tasks/delete/<int:task_id>/', views.delete_task, name='delete_task'),

    # Timer
    path('timer/', views.timer_view, name='timer'),
    path('timer/complete/', views.complete_session, name='complete_session'),

    # Flashcards
    path('flashcards/', views.flashcards_view, name='flashcards'),
    path('flashcards/deck/add/', views.add_deck, name='add_deck'),
    path('flashcards/deck/<int:deck_id>/study/', views.study_deck, name='study_deck'),
    path('flashcards/deck/<int:deck_id>/edit/', views.edit_deck, name='edit_deck'),
    path('flashcards/deck/<int:deck_id>/delete/', views.delete_deck, name='delete_deck'),
    path('flashcards/deck/<int:deck_id>/card/add/', views.add_card, name='add_card'),
    path('flashcards/card/<int:card_id>/edit/', views.edit_card, name='edit_card'),
    path('flashcards/card/<int:card_id>/delete/', views.delete_card, name='delete_card'),
    path('flashcards/card/<int:card_id>/mark/', views.mark_card, name='mark_card'),

    # Analytics
    path('analytics/', views.analytics_view, name='analytics'),

    # Calendar
    path('calendar/', views.calendar_view, name='calendar'),
    path('calendar/add/', views.add_event, name='add_event'),
    path('calendar/delete/<int:event_id>/', views.delete_event, name='delete_event'),
]
