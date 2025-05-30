import datetime
from django.db import models
from django.dispatch import receiver
from django.utils import timezone
from django.contrib import admin
from django.contrib.auth.models import User
from django.db.models import F
from django.db.models.signals import post_delete, post_save
# Create your models here.


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published", default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.question_text

    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Recently published?",
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class Vote(models.Model):
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    voter = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.voter} voted for {self.choice}"


@receiver(post_save, sender=Vote)
def increment_choice_votes(sender, instance, created, **kwargs):
    if created:
        instance.choice.votes = F("votes") + 1
        instance.choice.save()


@receiver(post_delete, sender=Vote)
def decrement_choice_votes(sender, instance, **kwargs):
    instance.choice.votes = F("votes") - 1
    instance.choice.save()
