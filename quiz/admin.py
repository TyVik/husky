from adminsortable.admin import SortableTabularInline, SortableAdmin
from django.contrib import admin

from quiz.models import Quiz, Question, Answer


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]


class QuestionInline(SortableTabularInline):
    model = Question
    extra = 0


@admin.register(Quiz)
class QuizAdmin(SortableAdmin):
    inlines = [QuestionInline]
