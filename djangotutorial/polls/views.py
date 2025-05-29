from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader
from django.db.models import F
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

import logging
from .models import Choice, Question
from .forms import QuestionForm, ChoiceFormSet

logger = logging.getLogger(__name__)

def get_past_question_or_404(pk):
    try:
        return Question.objects.get(pk=pk, pub_date__lte=timezone.now())
    except Question.DoesNotExist:
        logger.warning("No questions found with pub_date <= now")
        raise Http404("Question does not exist")

class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"
    paginate_by = 5
    login_url = 'login'
    def get_queryset(self):
        """Generates last five published questions

        Returns:
            list[Questions]: list of 5 questions
        """
        logger.info("Fetching the latest 5 published questions")

        queryset = Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by("-pub_date")

        if queryset.count() == 0:
            logger.warning("No questions found with pub_date <= now")
        else:
            logger.info(f"Fetched {queryset.count()} questions")

        return queryset

class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Question
    template_name = "polls/detail.html"
    login_url = 'login'
    def get_object(self):
        logger.info("Fetching details for Question ID %s", self.kwargs['pk'])
        question = get_past_question_or_404(self.kwargs['pk'])
        logger.info(f"Fetched question {question}")

        return question

class ResultsView(LoginRequiredMixin, generic.DetailView):
    model = Question
    template_name = "polls/results.html"
    login_url = 'login'
    def get_object(self):
        logger.info("Fetching Results for Question ID %s", self.kwargs['pk'])
        question = get_past_question_or_404(self.kwargs['pk'])

        logger.info(f"Fetched question {question}")

        return question

@login_required(login_url='login')
def add_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.pub_date = timezone.now()
            question.save()

            formset = ChoiceFormSet(request.POST, instance=question)
            if formset.is_valid():
                formset.save()
                return redirect('polls:index')
        else:
            formset = ChoiceFormSet(request.POST)
    else:
        form = QuestionForm()
        formset = ChoiceFormSet()

    return render(request, 'polls/add_question.html', {
        'form': form,
        'formset': formset
    })


# def index(request):
#     latest_question_list = Question.objects.order_by("-pub_date")[:5]
#     context = {
#         "latest_question_list": latest_question_list
#     }
#     # template = loader.get_template("polls/index.html")
#     # return HttpResponse(template.render(context, request))

#     # Shortcut for above
#     return render(request, "polls/index.html", context)

# def detail(request, question_id):
#     # try:
#     #     question = Question.objects.get(pk=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404("Question does not exist")

#     # Shortcut for above code
#     question = get_object_or_404(Question, pk=question_id)
#     return render(
#         request,
#         "polls/detail.html",
#         {
#             "question": question
#         }
#     )

# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(
#         request,
#         "polls/results.html",
#         {
#             "question": question
#         }
#     )

@login_required(login_url='login')
def vote(request, question_id):
    """
    Adds a vote to the selected choice and increase vote by 1.

    Args:
        request (_type_): _description_
        question_id (_type_): _description_

    Returns:
        _type_: _description_
    """
    logger.info(f"Voting for Question id: {question_id}")
    question = get_past_question_or_404(question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
        logger.info(f"Choice: {selected_choice}")
    except (KeyError, Choice.DoesNotExist):
        logger.warning(f"You didn't select a valid choice.")
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        logger.info(f"Votes increased")

        return HttpResponseRedirect(reverse("polls:results",args=(question_id,)))
