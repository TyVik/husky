from adminsortable.admin import SortableTabularInline, SortableAdmin
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet
from django.urls import reverse
from django.utils.safestring import mark_safe

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
    fields = ('text', 'link')
    readonly_fields = ('link',)
    extra = 0

    def link(self, obj):
        url = reverse('admin:quiz_question_change', args=(obj.id,))
        return mark_safe('<a href="{}">Link to question</a>'.format(url))


@admin.register(Quiz)
class QuizAdmin(SortableAdmin):
    inlines = [QuestionInline]


@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user', 'quiz')
    list_filter = ('user', 'quiz')  # use select2 widget for future
