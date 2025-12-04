from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note


# Константы для пользователей
AUTHOR_USERNAME = 'author'
READER_USERNAME = 'reader'
PASSWORD = 'testpass123'

# Константы для заметок
NOTE_SLUG = 'test-slug'
NOTE_TITLE = 'Test Note'
NOTE_TEXT = 'Test text'

# Константы URL (без параметров)
HOME_URL = reverse('notes:home')
LIST_URL = reverse('notes:list')
ADD_URL = reverse('notes:add')
SUCCESS_URL = reverse('notes:success')
LOGIN_URL = reverse('users:login')
SIGNUP_URL = reverse('users:signup')
LOGOUT_URL = reverse('users:logout')

# Данные для форм
FORM_DATA = {
    'title': NOTE_TITLE,
    'text': NOTE_TEXT,
    'slug': NOTE_SLUG,
}


class BaseTestCase(TestCase):
    """Базовый класс для всех тестов ya_note."""

    @classmethod
    def setUpTestData(cls):
        """Создание тестовых данных один раз для всего класса."""
        cls.author = User.objects.create_user(
            username=AUTHOR_USERNAME,
            password=PASSWORD
        )
        cls.reader = User.objects.create_user(
            username=READER_USERNAME,
            password=PASSWORD
        )

        cls.note = Note.objects.create(
            title=NOTE_TITLE,
            text=NOTE_TEXT,
            slug=NOTE_SLUG,
            author=cls.author
        )

        cls.note_detail_url = reverse('notes:detail', args=[NOTE_SLUG])
        cls.note_edit_url = reverse('notes:edit', args=[NOTE_SLUG])
        cls.note_delete_url = reverse('notes:delete', args=[NOTE_SLUG])

    def setUp(self):
        """Создание клиентов для каждого теста."""
        self.client = Client()
        self.author_client = Client()
        self.author_client.force_login(self.author)
        self.reader_client = Client()
        self.reader_client.force_login(self.reader)
        