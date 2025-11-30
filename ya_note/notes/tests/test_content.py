from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from notes.models import Note


class TestContent(TestCase):
    def test_add_page_contains_form(self):
        user = User.objects.create_user(username='alex', password='123')
        client = Client()
        client.login(username='alex', password='123')

        url = reverse('notes:add')  # если имя маршрута другое — замени
        response = client.get(url)

        # проверяем, что в контексте страницы есть объект формы
        self.assertIn('form', response.context)


from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from notes.models import Note


class TestContent(TestCase):
    def test_note_appears_in_notes_list(self):
        user = User.objects.create_user(username='alex', password='123')
        Note.objects.create(title='note1', text='some text', author=user)

        client = Client()
        client.login(username='alex', password='123')

        url = reverse('notes:list')  # проверь имя маршрута
        response = client.get(url)
        object_list = response.context['object_list']

        self.assertEqual(len(object_list), 1)
        self.assertEqual(object_list[0].title, 'note1')

