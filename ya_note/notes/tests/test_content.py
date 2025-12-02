from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from notes.models import Note


class TestContent(TestCase):
    def test_add_page_contains_form(self):
        User.objects.create_user(username='alex', password='123')
        client = Client()
        client.login(username='alex', password='123')

        url = reverse('notes:add')  # если имя маршрута другое — замени
        response = client.get(url)

        # проверяем, что в контексте страницы есть объект формы
        self.assertIn('form', response.context)


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


class TestContent(TestCase):
    def test_edit_page_contains_form(self):
        user = User.objects.create_user(username='alex', password='123')
        Note.objects.create(
            title='test note',
            text='text',
            author=user,
            slug='test-slug',
        )

        client = Client()
        client.login(username='alex', password='123')

        url = reverse('notes:edit', args=['test-slug'])
        response = client.get(url)

        self.assertIn('form', response.context)

    def test_notes_list_shows_only_user_notes(self):
        user1 = User.objects.create_user(username='alex', password='123')
        user2 = User.objects.create_user(username='kate', password='123')

        Note.objects.create(title='note1', text='text', author=user1)
        Note.objects.create(title='note2', text='text', author=user2)

        client = Client()
        client.login(username='alex', password='123')

        url = reverse('notes:list')
        response = client.get(url)
        object_list = response.context['object_list']

        # в списке должны быть только заметки user1
        self.assertEqual(len(object_list), 1)
        self.assertEqual(object_list[0].author, user1)
