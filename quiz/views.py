from django.views.generic import DetailView

from quiz.models import QuizResult


class QuizResultView(DetailView):
    model = QuizResult

    def get_queryset(self):
        return super(QuizResultView, self).get_queryset().filter(user_id=self.request.user.id)
