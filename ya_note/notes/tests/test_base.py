from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note


# Константа для slug заметки
NOTE_SLUG = 'existing-slug'

# Константы URL (без параметров)
HOME_URL = reverse('notes:home')
LIST_URL = reverse('notes:list')
ADD_URL = reverse('notes:add')
SUCCESS_URL = reverse('notes:success')
LOGIN_URL = reverse('users:login')
SIGNUP_URL = reverse('users:signup')
LOGOUT_URL = reverse('users:logout')

# Константы URL (с параметрами)
NOTE_DETAIL_URL = reverse('notes:detail', args=[NOTE_SLUG])
NOTE_EDIT_URL = reverse('notes:edit', args=[NOTE_SLUG])
NOTE_DELETE_URL = reverse('notes:delete', args=[NOTE_SLUG])

# URL для редиректов
LIST_REDIRECT_URL = f'{LOGIN_URL}?next={LIST_URL}'
ADD_REDIRECT_URL = f'{LOGIN_URL}?next={ADD_URL}'
SUCCESS_REDIRECT_URL = f'{LOGIN_URL}?next={SUCCESS_URL}'
NOTE_DETAIL_REDIRECT_URL = f'{LOGIN_URL}?next={NOTE_DETAIL_URL}'
NOTE_EDIT_REDIRECT_URL = f'{LOGIN_URL}?next={NOTE_EDIT_URL}'
NOTE_DELETE_REDIRECT_URL = f'{LOGIN_URL}?next={NOTE_DELETE_URL}'


class BaseTestCase(TestCase):
    """Базовый класс для всех тестов ya_note."""

    @classmethod
    def setUpTestData(cls):
        """Создание тестовых данных один раз для всего класса."""
        cls.author = User.objects.create_user(
            username='author',
            password='testpass123'
        )
        cls.reader = User.objects.create_user(
            username='reader',
            password='testpass123'
        )

        cls.note = Note.objects.create(
            title='Existing Note',
            text='Existing text',
            slug=NOTE_SLUG,
            author=cls.author
        )

        # Данные для создания новой заметки
        cls.form_data = {
            'title': 'New Note',
            'text': 'New text',
            'slug': 'new-slug',
        }
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)
