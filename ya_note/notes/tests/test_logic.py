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


    def test_cannot_create_two_notes_with_same_slug(self):
        user = User.objects.create_user(username='alex', password='123')
        client = Client()
        client.login(username='alex', password='123')

        # создаём первую заметку со slug
        Note.objects.create(
            title='note1',
            text='text1',
            author=user,
            slug='duplicate'
        )

        # пытаемся создать вторую заметку с тем же slug
        url = reverse('notes:add')
        data = {'title': 'note2', 'text': 'text2', 'slug': 'duplicate'}

        response = client.post(url, data)

        # slug уникальный → вторая заметка НЕ должна создаться
        self.assertEqual(Note.objects.filter(slug='duplicate').count(), 1)


    def test_slug_is_generated_automatically_if_not_provided(self):
        user = User.objects.create_user(username='alex', password='123')
        client = Client()
        client.login(username='alex', password='123')

        data = {
            'title': 'Моя заметка',
            'text': 'Текст заметки'
        }

        url = reverse('notes:add')
        client.post(url, data)

        # заметка должна создаться
        note = Note.objects.first()
        self.assertIsNotNone(note)

        # slug должен быть автоматически сформирован (не пустой)
        self.assertTrue(note.slug)
