from django.urls import path

from . import views

app_name = "polls"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote", views.vote, name="vote"),
    path("question/add/", views.add_question, name="add_question"),
    path("my/polls/", views.CreatedPollsView.as_view(), name="my_polls"),
    path('<int:pk>/delete/', views.QuestionDeleteView.as_view(), name='delete'),
    path('<int:pk>/edit/', views.edit_question, name='edit'),
]
