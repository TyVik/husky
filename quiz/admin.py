from adminsortable.admin import SortableTabularInline, SortableAdmin
from django.contrib import admin

from quiz.models import Quiz, Question, Answer, QuizResult


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


@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user', 'quiz')
    list_filter = ('user', 'quiz')  # use select2 widget for future
