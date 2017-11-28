from django.conf.urls import url

from quiz.views import QuizResultView

urlpatterns = [
    url(r'^result/(?P<pk>\d+)/$', QuizResultView.as_view(), name='result'),
]
