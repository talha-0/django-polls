# Create your tests here.
import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Question


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose
        pub_date is in future
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


def create_question(question_text, days):
    """Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).

    Args:
        question_text (str): text for creating function
        days (int): no of days for now negative for past positive for in future
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(
        question_text=question_text,
        pub_date=time
    )


class QuestionIndexViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass')

    def test_no_questions(self):
        """
        If no questions found , an appropriate message is displayed
        """
        self.client.login(
            username='testuser',
            password='testpass'
        )
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(
            response.status_code,
            200
        )
        self.assertContains(
            response,
            "No polls are available."
        )
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            []
        )

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        self.client.login(
            username='testuser',
            password='testpass'
        )
        question = create_question(
            question_text="Past question",
            days=-30
        )
        response = self.client.get(
            reverse("polls:index")
        )
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question]
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future are not displayed on
        the index page.
        """
        self.client.login(
            username='testuser',
            password='testpass'
        )
        question = create_question(
            question_text="Future question",
            days=30
        )
        response = self.client.get(
            reverse("polls:index")
        )
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            []
        )

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        self.client.login(
            username='testuser',
            password='testpass'
        )
        create_question(
            question_text="Future question",
            days=30
        )
        question = create_question(
            question_text="Past question",
            days=-30
        )
        response = self.client.get(
            reverse("polls:index")
        )
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question]
        )

    def test_future_question_and_past_question(self):
        """
        The index page may show multiple past questions.
        """
        self.client.login(
            username='testuser',
            password='testpass'
        )
        question1 = create_question(
            question_text="Past question 1.",
            days=-5
        )
        question2 = create_question(
            question_text="Past question 2.",
            days=-30
        )
        response = self.client.get(
            reverse("polls:index")
        )
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question1, question2]
        )


class QuestionDetailViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass')

    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        self.client.login(
            username='testuser',
            password='testpass'
        )
        future_question = create_question(
            question_text="Future question.",
            days=30
        )
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        self.client.login(
            username='testuser',
            password='testpass'
        )
        past_question = create_question(
            question_text="Future question.",
            days=-30
        )
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
