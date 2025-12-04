from django.contrib.auth.models import User

from notes.models import Note

from .test_base import BaseTestCase, ADD_URL, FORM_DATA


class TestLogic(BaseTestCase):

    def test_authenticated_user_can_create_note(self):
        form_data = {
            'title': 'New note',
            'text': 'New text',
            'slug': 'new-slug'
        }

        self.author_client.post(ADD_URL, data=form_data)

        self.assertEqual(Note.objects.count(), 2)

        new_note = Note.objects.get(slug='new-slug')
        self.assertEqual(new_note.title, form_data['title'])
        self.assertEqual(new_note.text, form_data['text'])
        self.assertEqual(new_note.slug, form_data['slug'])
        self.assertEqual(new_note.author, self.author)

    def test_cannot_create_two_notes_with_same_slug(self):
        form_data = {
            'title': 'Another note',
            'text': 'Another text',
            'slug': self.note.slug
        }

        self.author_client.post(ADD_URL, data=form_data)

        self.assertEqual(Note.objects.count(), 1)

    def test_slug_is_generated_automatically_if_not_provided(self):
        form_data = {
            'title': 'Моя заметка',
            'text': 'Текст заметки'
        }

        self.author_client.post(ADD_URL, data=form_data)

        self.assertEqual(Note.objects.count(), 2)

        new_note = Note.objects.get(title='Моя заметка')
        self.assertEqual(new_note.title, form_data['title'])
        self.assertEqual(new_note.text, form_data['text'])
        self.assertEqual(new_note.author, self.author)
        self.assertTrue(new_note.slug)
        self.assertEqual(new_note.slug, 'moya-zametka')

    def test_anonymous_user_cannot_create_note(self):
        form_data = {
            'title': 'Anon note',
            'text': 'Anon text',
            'slug': 'anon-slug'
        }

        self.client.post(ADD_URL, data=form_data)

        self.assertEqual(Note.objects.count(), 1)

    def test_user_can_edit_own_note(self):
        form_data = {
            'title': 'Edited title',
            'text': 'Edited text',
            'slug': self.note.slug
        }

        self.author_client.post(self.note_edit_url, data=form_data)

        updated_note = Note.objects.get(slug=self.note.slug)
        self.assertEqual(updated_note.title, form_data['title'])
        self.assertEqual(updated_note.text, form_data['text'])
        self.assertEqual(updated_note.slug, form_data['slug'])
        self.assertEqual(updated_note.author, self.author)

    def test_user_can_delete_own_note(self):
        self.author_client.post(self.note_delete_url)

        self.assertEqual(Note.objects.count(), 0)

    def test_user_cannot_edit_other_user_note(self):
        form_data = {
            'title': 'Hacked title',
            'text': 'Hacked text',
            'slug': self.note.slug
        }

        self.reader_client.post(self.note_edit_url, data=form_data)

        unchanged_note = Note.objects.get(slug=self.note.slug)
        self.assertEqual(unchanged_note.title, self.note.title)
        self.assertEqual(unchanged_note.text, self.note.text)
        self.assertEqual(unchanged_note.slug, self.note.slug)
        self.assertEqual(unchanged_note.author, self.note.author)

    def test_user_cannot_delete_other_user_note(self):
        self.reader_client.post(self.note_delete_url)

        self.assertEqual(Note.objects.count(), 1)
        self.assertTrue(Note.objects.filter(slug=self.note.slug).exists())
