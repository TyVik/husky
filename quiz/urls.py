from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from quiz.views import QuizResultView, QuizView, QuestionView

urlpatterns = [
    url(r'^result/(?P<pk>\d+)/$', login_required(QuizResultView.as_view()), name='result'),
    url(r'^(?P<pk>\d+)/$', login_required(QuizView.as_view()), name='quiz'),
    url(r'^(?P<quiz_id>\d+)/question/(?P<question_num>\d+)/$', login_required(QuestionView.as_view()), name='question'),
]
