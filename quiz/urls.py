from django.conf.urls import url

from quiz.views import QuizResultView, QuizView

urlpatterns = [
    url(r'^result/(?P<pk>\d+)/$', QuizResultView.as_view(), name='result'),
    url(r'^start/(?P<pk>\d+)/$', QuizView.as_view(), name='start'),
]
