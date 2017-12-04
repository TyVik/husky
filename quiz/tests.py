import random

from django.conf import settings
from django.contrib.auth import get_user_model, get_user
from django.test import TestCase, Client
from django.urls import reverse
from django.utils.crypto import get_random_string

from quiz.models import Quiz, Question, Answer, QuizResult


class IndexTestCase(TestCase):
    def setUp(self):
        super(IndexTestCase, self).setUp()
        self.client = Client()

    @classmethod
    def setUpTestData(cls):
        super(IndexTestCase, cls).setUpTestData()
        cls.credentials = {'username': get_random_string(6), 'password': get_random_string(6)}
        cls.user = get_user_model().objects.create_user(**cls.credentials)

    def test_index(self):
        url = reverse('index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertContains(response, 'Need')

        self.client.login(**self.credentials)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertContains(response, 'table')


class QuizTestCase(TestCase):
    def setUp(self):
        super(QuizTestCase, self).setUp()
        self.client = Client()

    @classmethod
    def setUpTestData(cls):
        super(QuizTestCase, cls).setUpTestData()
        cls.credentials = {'username': get_random_string(6), 'password': get_random_string(6)}
        cls.user = get_user_model().objects.create_user(**cls.credentials)
        cls.quizzes = [Quiz.objects.create(title=get_random_string(10)) for _ in range(5)]

    def check_auth(self, url):
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '{}?next={}'.format(reverse(settings.LOGIN_URL), url))

    def test_index(self):
        url = reverse('index')
        self.client.login(**self.credentials)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        for quiz in self.quizzes:
            self.assertContains(response, quiz.title)
            self.assertContains(response, reverse('quiz', kwargs={'pk': quiz.id}))

    def test_quiz(self):
        url = reverse('quiz', kwargs={'pk': self.quizzes[0].id})
        self.check_auth(url)

        self.client.login(**self.credentials)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quiz/quiz_detail.html')

    def test_integration(self):
        def generate_question(quiz: Quiz, order: int) -> Question:
            question = Question.objects.create(quiz=quiz, text=get_random_string(30), order=order)
            [Answer.objects.create(question=question, text=get_random_string(10), is_correct=random.getrandbits(1))
             for _ in range(2)]
            return question

        def get_answer(question: Question, index: int) -> Answer:
            return question.answer_set.order_by('id').all()[index]

        def only_first_answer_is_correct(question: Question) -> bool:
            return get_answer(question, 0).is_correct and not get_answer(question, 1).is_correct

        self.client.login(**self.credentials)
        quiz = random.choice(self.quizzes)
        quiz_result = None
        QUESTION_COUNT = 5
        questions = [generate_question(quiz, order) for order in range(QUESTION_COUNT)]
        for i in range(QUESTION_COUNT):
            index = i + 1
            data = {'answers': [get_answer(questions[i], 0).id]}  # only if first answer is correct
            response = self.client.post(reverse('question', kwargs={'quiz_id': quiz.id, 'question_num': index}), data)
            self.assertEqual(response.status_code, 302)
            if index == QUESTION_COUNT:
                quiz_result = QuizResult.objects.get(quiz=quiz, user=get_user(self.client))
                self.assertEqual(response.url, reverse('result', kwargs={'pk': quiz_result.id}))
            else:
                self.assertEqual(response.url, reverse('question', kwargs={'quiz_id': quiz.id, 'question_num': index + 1}))
        # check quiz result
        self.assertEqual(quiz_result.correct + quiz_result.wrong, QUESTION_COUNT)
        self.assertEqual(int(quiz_result.correct * 100 / (quiz_result.correct + quiz_result.wrong)), quiz_result.percent)
        print(quiz_result.answers)
        self.assertEqual(quiz_result.correct, len([question.id for question in questions if only_first_answer_is_correct(question)]))
