from typing import Tuple

from django.db.models import Model, QuerySet
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import DetailView

from quiz.models import QuizResult, Quiz, Question, Answer


class AlreadySolvedException(Exception):
    def __init__(self, quiz_result: QuizResult):
        self.quiz_result = quiz_result

    @property
    def redirect_url(self) -> str:
        return self.quiz_result.get_absolute_url()


class BaseQuizzesView(DetailView):
    def dispatch(self, request, *args, **kwargs):
        try:
            return super(BaseQuizzesView, self).dispatch(request, *args, **kwargs)
        except AlreadySolvedException as e:
            return HttpResponseRedirect(e.redirect_url)

    def check_user_permissions(self, obj: Model) -> None:
        raise NotImplementedError


class QuizResultView(DetailView):
    model = QuizResult

    def get_queryset(self) -> QuerySet:
        return super(QuizResultView, self).get_queryset().filter(user_id=self.request.user.id)


class QuizView(BaseQuizzesView):
    model = Quiz

    def get_object(self, queryset=None) -> Model:
        obj = super(QuizView, self).get_object(queryset)
        self.check_user_permissions(obj)
        return obj

    def check_user_permissions(self, obj: Quiz) -> None:
        quiz_result = obj.quizresult_set.filter(user=self.request.user).first()
        if quiz_result is not None:
            raise AlreadySolvedException(quiz_result)


class QuestionView(BaseQuizzesView):
    model = Question

    def get_object(self, queryset=None) -> Question:
        if queryset is None:
            queryset = self.get_queryset()

        try:
            queryset = queryset.filter(quiz_id=self.kwargs['quiz_id'])
            obj = queryset[int(self.kwargs['question_num']) - 1]
        except:
            # Yes, catch all exceptions. Do not show user invalid result.
            # It can be meaningful to divide by 2 conditions: for wrong parameters and for access denied.
            raise Http404('Sorry, wrong question')
        self.check_user_permissions(obj)
        return obj

    def check_user_permissions(self, obj: Question) -> None:
        quiz_result = obj.quiz.quizresult_set.filter(user=self.request.user).first()
        if quiz_result is not None:
            raise AlreadySolvedException(quiz_result)

    def post(self, request, quiz_id: str, question_num: str, *args, **kwargs) -> HttpResponseRedirect:
        def check_correct() -> Tuple[int, bool]:
            obj = self.get_object()
            answers = map(int, request.POST.getlist('answers', []))
            corrects = Answer.objects.filter(question=obj, is_correct=True).values_list('id', flat=True)
            return obj.id, set(answers) == set(corrects)

        def save_result_to_session(question_id: int, result: bool) -> None:
            if 'answers' not in request.session:
                request.session['answers'] = {}
            request.session['answers'][question_id] = result
            request.session.save()

        # keep in mind situation when admin changing question
        save_result_to_session(*check_correct())
        question_num = int(question_num)
        if Question.objects.filter(quiz_id=quiz_id).count() == question_num:
            # For production I'll create my own session storage (based on default) for working with answers.
            # Next line must be encapsulated into session object.
            answers = {int(key): value for key, value in request.session['answers'].items()}
            quiz_result = QuizResult.create_from_answers(
                quiz_id=int(quiz_id), user_id=request.user.id, answers=answers)
            url = quiz_result.get_absolute_url()
        else:
            url = reverse('question', kwargs={'quiz_id': quiz_id, 'question_num': question_num + 1})
        return HttpResponseRedirect(url)  # yes, I know about unnecessary request, but it's just for demo
