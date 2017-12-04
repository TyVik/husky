from django.conf import settings
from django.contrib.auth import get_user, get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from django.utils.crypto import get_random_string


class RegistrationTestCase(TestCase):
    def setUp(self):
        super(RegistrationTestCase, self).setUp()
        self.client = Client()
        self.url = reverse('registration')

    def test_registration(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/registration.html')

        password = get_random_string(6)
        username = get_random_string(6)
        response = self.client.post(self.url, {'username': username, 'password1': password, 'password2': password})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, settings.LOGIN_REDIRECT_URL)
        user = get_user(response.client)
        user_in_db = get_user_model().objects.get(username=username)
        self.assertEqual(user.id, user_in_db.id)


class UserTestCase(TestCase):
    def setUp(self):
        super(UserTestCase, self).setUp()
        self.client = Client()

    @classmethod
    def setUpTestData(cls):
        super(UserTestCase, cls).setUpTestData()
        cls.credentials = {'username': get_random_string(6), 'password': get_random_string(6)}
        cls.user = get_user_model().objects.create_user(**cls.credentials)

    def test_logout(self):
        self.client.login(**self.credentials)
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, settings.LOGOUT_REDIRECT_URL)
        self.assertTrue(get_user(response.client).is_anonymous)

    def test_login(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

        response = self.client.post(reverse('login'), self.credentials)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(get_user(response.client), self.user)
