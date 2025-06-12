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
    path("questions/user/", views.user_questions, name="user_questions"),
    # Choices
    path("choices/", views.list_choices, name="list_choices"),
    path("choices/add/", views.create_choice, name="create_choice"),
    path("choices/<int:pk>/", views.list_question_choices, name="list_choices"),
    # Votes
    path("votes/", views.list_votes, name="list_votes"),
    path("vote/", views.cast_vote, name="cast_vote"),
]

# from django.urls import path
# from .views import (
#     ListQuestionsView, QuestionDetailView, CreateQuestionView, UpdateQuestionView, DeleteQuestionView,
#     ListChoicesView, CreateChoiceView, QuestionChoicesView, QuestionResultsView,
#     ListVotesView, CastVoteView
# )

# urlpatterns = [
#     path("questions/", ListQuestionsView.as_view(), name="list_questions"),
#     path("questions/<int:pk>/", QuestionDetailView.as_view(), name="question_detail"),
#     path("questions/create/", CreateQuestionView.as_view(), name="create_question"),
#     path("questions/<int:pk>/edit/", UpdateQuestionView.as_view(), name="update_question"),
#     path("questions/<int:pk>/delete/", DeleteQuestionView.as_view(), name="delete_question"),
#     path("choices/", ListChoicesView.as_view(), name="list_choices"),
#     path("choices/create/", CreateChoiceView.as_view(), name="create_choice"),
#     path("questions/<int:pk>/choices/", QuestionChoicesView.as_view(), name="question_choices"),
#     path("questions/<int:pk>/results/", QuestionResultsView.as_view(), name="question_results"),
#     path("votes/", ListVotesView.as_view(), name="list_votes"),
#     path("votes/cast/", CastVoteView.as_view(), name="cast_vote"),
# ]
