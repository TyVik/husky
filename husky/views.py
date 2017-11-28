from django.db import connection
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from husky.utils import namedtuple_fetchall


def index(request: HttpRequest) -> HttpResponse:
    with connection.cursor() as cursor:
        cursor.execute("""select q.id id, q.title title, r.created created from quiz_quiz q LEFT OUTER JOIN 
            (select quiz_id, created from quiz_quizresult where user_id = %s) r on (r.quiz_id = q.id)""",
                       (request.user.id,))
        quizzes = namedtuple_fetchall(cursor)
    return render(request, 'index.html', context={'quizzes': quizzes})
