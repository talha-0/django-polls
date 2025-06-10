from django.urls import path
from . import views

urlpatterns = [
    path("questions/", views.getData, name="get_questions"),
    path("questions/add/", views.addItem, name="add_question"),
    path("choices/", views.getChoices, name="get_choices"),
    path("vote/", views.castVote, name="cast_vote"),
]
