from django.contrib import admin

from .models import Choice, Question, Vote


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    list_display = ["question_text", "pub_date", "was_published_recently"]
    fieldsets = [
        (None, {"fields": ["question_text", "author"]}),
        ("Date information", {"fields": ["pub_date"]}),
    ]
    inlines = [ChoiceInline]
    list_filter = ["pub_date"]
    search_fields = ["question_text"]


class VotesInline(admin.TabularInline):
    model = Vote
    extra = 0


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ["choice_text", "votes", "question"]
    inlines = [VotesInline]


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Vote)
