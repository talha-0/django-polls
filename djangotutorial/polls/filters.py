import django_filters

from .models import Question


class QuestionFilter(django_filters.FilterSet):
    question_text = django_filters.CharFilter(lookup_expr="icontains", label="Search")

    class Meta:
        model = Question
        fields = ["question_text"]
