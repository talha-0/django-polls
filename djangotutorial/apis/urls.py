from django.urls import path

from . import views

urlpatterns = [
    # Questions
    path("questions/", views.list_questions, name="list_questions"),
    path("questions/add/", views.create_question, name="create_question"),
    path("questions/<int:pk>/update/", views.update_question, name="update_question"),
    path("questions/<int:pk>/delete/", views.delete_question, name="delete_question"),
    path("questions/<int:pk>/", views.question_detail, name="question_detail"),
    path(
        "questions/<int:pk>/results/", views.question_results, name="question_results"
    ),
    # Choices
    path("choices/", views.list_choices, name="list_choices"),
    path("choices/add/", views.create_choice, name="create_choice"),
    path("choices/<int:pk>/", views.list_question_choices, name="list_choices"),
    # Votes
    path("votes/", views.list_votes, name="list_votes"),
    path("vote/", views.cast_vote, name="cast_vote"),
]
