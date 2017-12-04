from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from django.utils.crypto import get_random_string

from quiz.models import Quiz


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

        quizzes = [Quiz.objects.create(title=get_random_string(10)) for _ in range(5)]
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        for quiz in quizzes:
            self.assertContains(response, quiz.title)
            self.assertContains(response, reverse('quiz', kwargs={'pk': quiz.id}))
