from notes.forms import NoteForm
from notes.models import Note

from .test_base import BaseTestCase, ADD_URL, LIST_URL


class TestContent(BaseTestCase):

    def test_forms_available_on_pages(self):
        """Проверка наличия формы на страницах добавления и редактирования."""
        urls = [ADD_URL, self.note_edit_url]

        for url in urls:
            with self.subTest(url=url):
                response = self.author_client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)

    def test_note_appears_in_notes_list(self):
        response = self.author_client.get(LIST_URL)
        notes = response.context['object_list']

        self.assertIn(self.note, notes)
        self.assertEqual(self.note.title, 'Test Note')
        self.assertEqual(self.note.text, 'Test text')
        self.assertEqual(self.note.slug, 'test-slug')
        self.assertEqual(self.note.author, self.author)

    def test_notes_list_shows_only_user_notes(self):
        reader_note = Note.objects.create(
            title='Reader note',
            text='Reader text',
            slug='reader-slug',
            author=self.reader
        )

        response = self.author_client.get(LIST_URL)
        notes = response.context['object_list']

        self.assertIn(self.note, notes)
        self.assertNotIn(reader_note, notes)
        self.assertEqual(len(notes), 1)
