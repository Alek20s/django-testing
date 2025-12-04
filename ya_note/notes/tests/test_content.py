from notes.forms import NoteForm

from .test_base import BaseTestCase, ADD_URL, LIST_URL, NOTE_EDIT_URL


class TestContent(BaseTestCase):

    def test_forms_available_on_pages(self):
        """Проверка наличия формы на страницах добавления и редактирования."""
        urls = [ADD_URL, NOTE_EDIT_URL]

        for url in urls:
            with self.subTest(url=url):
                response = self.author_client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)

    def test_note_appears_in_notes_list(self):
        response = self.author_client.get(LIST_URL)
        notes = response.context['object_list']
        self.assertIn(self.note, notes)

    def test_notes_list_shows_only_user_notes(self):
        response = self.reader_client.get(LIST_URL)
        notes = response.context['object_list']
        self.assertNotIn(self.note, notes)
