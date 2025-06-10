from polls.models import Choice, Question, Vote
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import QuestionSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getData(request):
    questions = Question.objects.all()
    serializer = QuestionSerializer(questions, many=True)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def addItem(request):
    serializer = QuestionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(author=request.user)
    return Response(serializer.data)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getChoices(request):
    choices = Choice.objects.all()
    data = [{"id": c.id, "choice_text": c.choice_text, "votes": c.votes, "question": c.question.id} for c in choices]
    return Response(data)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def castVote(request):
    choice_id = request.data.get("choice_id")
    try:
        choice = Choice.objects.get(id=choice_id)
        Vote.objects.create(choice=choice, voter=request.user)
        return Response({"message": "Vote cast successfully"}, status=status.HTTP_201_CREATED)
    except Choice.DoesNotExist:
        return Response({"error": "Choice not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
