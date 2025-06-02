import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import generic

from .filters import QuestionFilter
from .forms import ChoiceFormSet, QuestionForm
from .models import Choice, Question, Vote

logger = logging.getLogger(__name__)


def get_past_question_or_404(pk):
    try:
        return Question.objects.get(pk=pk, pub_date__lte=timezone.now())
    except Question.DoesNotExist:
        logger.warning("No questions found with pub_date <= now")
        raise Http404("No questions found with pub_date <= now")


class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"
    paginate_by = 5
    login_url = "login"

    def get_queryset(self):
        """Generates last published questions

        Returns:
            list[Questions]: list of questions
        """
        logger.info("Fetching the latest published questions")

        queryset = Question.objects.filter(pub_date__lte=timezone.now()).order_by(
            "-pub_date"
        )
        self.filterset = QuestionFilter(self.request.GET, queryset=queryset)
        filtered_qs = self.filterset.qs

        if queryset.count() == 0:
            logger.warning("No questions found with pub_date <= now")
        else:
            logger.info(f"Fetched {queryset.count()} questions")

        return filtered_qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = self.filterset
        return context


class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Question
    template_name = "polls/detail.html"
    login_url = "login"

    def get_object(self):
        logger.info("Fetching details for Question ID %s", self.kwargs["pk"])
        question = get_past_question_or_404(self.kwargs["pk"])
        logger.info(f"Fetched question {question}")

        return question


class ResultsView(LoginRequiredMixin, generic.DetailView):
    model = Question
    template_name = "polls/results.html"
    login_url = "login"

    def get_object(self):
        logger.info("Fetching Results for Question ID %s", self.kwargs["pk"])
        question = get_past_question_or_404(self.kwargs["pk"])

        logger.info(f"Fetched question {question}")

        return question


@login_required(login_url="login")
def add_question(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.pub_date = timezone.now()
            formset = ChoiceFormSet(request.POST, instance=question)

            if formset.is_valid():
                question.save()
                formset.save()
                return redirect("polls:index")
        else:
            formset = ChoiceFormSet(request.POST)
    else:
        form = QuestionForm()
        formset = ChoiceFormSet()

    return render(
        request, "polls/add_question.html", {"form": form, "formset": formset}
    )


class CreatedPollsView(LoginRequiredMixin, generic.ListView):
    template_name = "polls/my_polls.html"
    context_object_name = "latest_question_list"
    paginate_by = 5
    login_url = "login"

    def get_queryset(self):
        """Generates last questions

        Returns:
            list[Questions]: list of questions
        """
        logger.info("Fetching the latest questions")

        queryset = Question.objects.filter(author=self.request.user).order_by(
            "-pub_date"
        )

        if queryset.count() == 0:
            logger.warning("No questions found")
        else:
            logger.info(f"Fetched {queryset.count()} questions")

        return queryset


from django.http import HttpResponseForbidden


class QuestionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Question
    template_name = "polls/confirm_delete.html"
    success_url = reverse_lazy("polls:my_polls")
    login_url = "login"

    def dispatch(self, request, *args, **kwargs):
        question = self.get_object()
        if question.author != request.user:
            return HttpResponseForbidden("You are not allowed to delete this question.")
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


@login_required(login_url="login")
def edit_question(request, pk):
    question = get_object_or_404(Question, pk=pk, author=request.user)

    if Vote.objects.filter(choice__question=question).exists():
        messages.error(
            request, "Cannot edit this question because it has received votes."
        )
        return redirect("polls:my_polls")

    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        formset = ChoiceFormSet(request.POST, instance=question)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, "Question and choices updated successfully.")
            return redirect("polls:my_polls")
        else:
            print("Form errors:", form.errors)
            print(form)
            print("Formset errors:", formset.errors)
            print(formset)
            messages.error(
                request, "There was an error updating the question or choices."
            )
    else:
        form = QuestionForm(instance=question)
        formset = ChoiceFormSet(instance=question)

    return render(
        request, "polls/add_question.html", {"form": form, "formset": formset}
    )


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


@login_required(login_url="login")
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
    if Vote.objects.filter(voter=request.user, choice__question=question).exists():
        logger.warning(
            f"User {request.user.username} has already voted for this question."
        )
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You have already voted on this question.",
            },
        )

    Vote.objects.create(choice=selected_choice, voter=request.user)
    logger.info("Vote recorded successfully.")

    return HttpResponseRedirect(reverse("polls:results", args=(question_id,)))
