from django.forms.models import inlineformset_factory

from django import forms

from .models import Choice, Question


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["question_text"]


ChoiceFormSet = inlineformset_factory(
    Question,
    Choice,
    fields=["choice_text"],
    extra=0,
    min_num=1,
    validate_min=True,
    can_delete=True,
)
