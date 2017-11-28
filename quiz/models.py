from adminsortable.models import SortableMixin
from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models


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
    # answers = JSONField()  # avoid direct references to Answers. It's allow to manipulate them.

    def __str__(self):
        return 'QuizResult: {}'.format(self.id)
