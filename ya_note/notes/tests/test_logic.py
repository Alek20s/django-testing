from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from notes.models import Note


class TestLogic(TestCase):
    def test_authenticated_user_can_create_note(self):
        user = User.objects.create_user(username='alex', password='123')
        client = Client()
        client.login(username='alex', password='123')

        url = reverse('notes:add')  # если маршрут другой — замени
        data = {'title': 'test note', 'text': 'some text'}
        response = client.post(url, data)

        # проверяем, что заметка создалась
        self.assertTrue(Note.objects.filter(title='test note', author=user).exists())
