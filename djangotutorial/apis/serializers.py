from django.contrib.auth.models import User
from polls.models import Choice, Question, Vote
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username"
        ]


class QuestionSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Question
        fields = "__all__"


class ChoiceSerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all())

    class Meta:
        model = Choice
        fields = "__all__"


class VoteSerializer(serializers.ModelSerializer):
    voter = UserSerializer(read_only=True)
    choice = serializers.PrimaryKeyRelatedField(queryset=Choice.objects.all())

    class Meta:
        model = Vote
        fields = "__all__"
