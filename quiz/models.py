from typing import Dict

from adminsortable.models import SortableMixin
from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.urls import reverse


class Quiz(models.Model):
    title = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Quiz'
        verbose_name_plural = 'Quizzes'

    def __str__(self):
        return self.title


class Question(SortableMixin, models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    order = models.PositiveSmallIntegerField(default=0, editable=False, db_index=True)

    class Meta:
        ordering = ('order',)

    def __str__(self):
        return self.text[:20]


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=150)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text[:20]


class QuizResult(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    answers = JSONField()  # avoid direct references to Answers. It's allow to manipulate them.

    def __str__(self):
        return 'QuizResult: {}'.format(self.id)

    @staticmethod
    def create_from_answers(quiz_id: int, user_id: int, answers: Dict[int, bool]) -> 'QuizResult':
        result = QuizResult(answers={'correct': 0, 'wrong': 0, 'statistic': {}}, quiz_id=quiz_id, user_id=user_id)
        for question_id in Question.objects.filter(quiz_id=quiz_id).values_list('id', flat=True):
            answer = answers.get(question_id, False)
            if answer:
                result.answers['correct'] += 1
            else:
                result.answers['wrong'] += 1
            result.answers['statistic'][question_id] = answer
        result.save()
        return result

    def get_absolute_url(self):
        return reverse('result', kwargs={'pk': self.id})

    @property
    def total(self):
        correct, wrong = self.answers['correct'], self.answers['wrong']
        return {
            'correct': correct,
            'wrong': wrong,
            'percent': int(correct * 100 / (wrong + correct))
        }