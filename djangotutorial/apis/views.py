from django.utils import timezone
from polls.models import Choice, Question, Vote
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import ChoiceSerializer, QuestionSerializer, VoteSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_questions(request):
    questions = Question.objects.filter(pub_date__lte=timezone.now()).order_by(
        "-pub_date"
    )
    paginator = PageNumberPagination()
    paginator.page_size = 7
    result_page = paginator.paginate_queryset(questions, request)
    serializer = QuestionSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def question_detail(request, pk):
    try:
        question = Question.objects.get(pk=pk, pub_date__lte=timezone.now())
        serializer = QuestionSerializer(question)
        return Response(serializer.data)
    except Question.DoesNotExist:
        return Response(
            {"error": "Question not found or not published yet"},
            status=status.HTTP_404_NOT_FOUND,
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_question(request):
    choices_data = request.data.pop("choices", [])
    serializer = QuestionSerializer(data=request.data)
    if serializer.is_valid():
        question = serializer.save(author=request.user, pub_date=timezone.now())
        for choice_text in choices_data:
            Choice.objects.create(question=question, choice_text=choice_text)
        return Response(
            QuestionSerializer(question).data, status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def update_question(request, pk):
    try:
        question = Question.objects.get(pk=pk, author=request.user)
    except Question.DoesNotExist:
        return Response(
            {"error": "Question not found or not owned by user"},
            status=status.HTTP_404_NOT_FOUND,
        )

    if Vote.objects.filter(choice__question=question).exists():
        return Response(
            {"error": "Cannot edit this question because it has received votes."},
            status=status.HTTP_403_FORBIDDEN,
        )

    serializer = QuestionSerializer(question, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_question(request, pk):
    try:
        question = Question.objects.get(pk=pk, author=request.user)
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Question.DoesNotExist:
        return Response(
            {"error": "Question not found"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_choices(request):
    choices = Choice.objects.all()
    serializer = ChoiceSerializer(choices, many=True)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_choice(request):
    serializer = ChoiceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_question_choices(request, pk):
    try:
        question = Question.objects.get(pk=pk, pub_date__lte=timezone.now())
    except Question.DoesNotExist:
        return Response(
            {"error": "Question not found"}, status=status.HTTP_404_NOT_FOUND
        )

    choices = question.choice_set.all()
    serializer = ChoiceSerializer(choices, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def question_results(request, pk):
    try:
        question = Question.objects.get(pk=pk, pub_date__lte=timezone.now())
        choices = question.choice_set.all()
        results = [
            {"choice_text": choice.choice_text, "votes": choice.vote_set.count()}
            for choice in choices
        ]
        return Response({"question": question.question_text, "results": results})
    except Question.DoesNotExist:
        return Response(
            {"error": "Question not found"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_votes(request):
    votes = Vote.objects.all()
    serializer = VoteSerializer(votes, many=True)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def cast_vote(request):
    choice_id = request.data.get("choice")
    try:
        choice = Choice.objects.select_related("question").get(id=choice_id)
        question = choice.question

        if question.pub_date > timezone.now():
            return Response(
                {"error": "Voting is not allowed yet for this question."},
                status=status.HTTP_403_FORBIDDEN,
            )

        if Vote.objects.filter(voter=request.user, choice__question=question).exists():
            return Response(
                {"error": "You have already voted on this question."},
                status=status.HTTP_403_FORBIDDEN,
            )

        vote = Vote.objects.create(choice=choice, voter=request.user)
        return Response(VoteSerializer(vote).data, status=status.HTTP_201_CREATED)
    except Choice.DoesNotExist:
        return Response({"error": "Choice not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
