from django.conf.urls import url

from quiz.views import QuizResultView, QuizView, QuestionView

urlpatterns = [
    url(r'^result/(?P<pk>\d+)/$', QuizResultView.as_view(), name='result'),
    url(r'^(?P<pk>\d+)/$', QuizView.as_view(), name='quiz'),
    url(r'^(?P<quiz_id>\d+)/question/(?P<question_num>\d+)/$', QuestionView.as_view(), name='question'),
]
