from django.views.generic import DetailView

from quiz.models import QuizResult, Quiz


class QuizResultView(DetailView):
    model = QuizResult

    def get_queryset(self):
        return super(QuizResultView, self).get_queryset().filter(user_id=self.request.user.id)


class QuizView(DetailView):
    model = Quiz