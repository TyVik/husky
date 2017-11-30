from adminsortable.admin import SortableTabularInline, SortableAdmin
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from quiz.models import Quiz, Question, Answer, QuizResult


class AnswerFormSet(BaseInlineFormSet):
    def clean(self):
        super(AnswerFormSet, self).clean()
        for form in self.forms:
            if form.cleaned_data.get('is_correct', False):
                return
        raise ValidationError('Need at least one correct answer.')


class AnswerInline(admin.TabularInline):
    model = Answer
    formset = AnswerFormSet
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
