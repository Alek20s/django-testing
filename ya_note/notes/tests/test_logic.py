from pytils.translit import slugify

from notes.models import Note

from .test_base import BaseTestCase, ADD_URL, NOTE_EDIT_URL, NOTE_DELETE_URL


class TestLogic(BaseTestCase):

    def test_authenticated_user_can_create_note(self):
        initial_count = Note.objects.count()
        
        self.author_client.post(ADD_URL, data=self.form_data)

        self.assertEqual(Note.objects.count(), initial_count + 1)

        new_note = Note.objects.get(slug=self.form_data['slug'])
        self.assertEqual(new_note.title, self.form_data['title'])
        self.assertEqual(new_note.text, self.form_data['text'])
        self.assertEqual(new_note.slug, self.form_data['slug'])
        self.assertEqual(new_note.author, self.author)

    def test_cannot_create_two_notes_with_same_slug(self):
        form_data = self.form_data.copy()
        form_data['slug'] = self.note.slug

        notes_before = set(Note.objects.values_list('id', flat=True))

        self.author_client.post(ADD_URL, data=form_data)

        notes_after = set(Note.objects.values_list('id', flat=True))
        self.assertEqual(notes_before, notes_after)

    def test_slug_is_generated_automatically_if_not_provided(self):
        form_data = self.form_data.copy()
        form_data['title'] = 'Моя заметка'
        del form_data['slug']

        initial_count = Note.objects.count()
        
        self.author_client.post(ADD_URL, data=form_data)

        self.assertEqual(Note.objects.count(), initial_count + 1)

        new_note = Note.objects.get(title='Моя заметка')
        expected_slug = slugify(form_data['title'])
        self.assertEqual(new_note.title, form_data['title'])
        self.assertEqual(new_note.text, form_data['text'])
        self.assertEqual(new_note.author, self.author)
        self.assertEqual(new_note.slug, expected_slug)

    def test_anonymous_user_cannot_create_note(self):
        notes_before = set(Note.objects.values_list('id', flat=True))
        
        self.client.post(ADD_URL, data=self.form_data)

        notes_after = set(Note.objects.values_list('id', flat=True))
        self.assertEqual(notes_before, notes_after)

    def test_user_can_edit_own_note(self):
        form_data = self.form_data.copy()
        form_data['slug'] = self.note.slug

        self.author_client.post(NOTE_EDIT_URL, data=form_data)

        updated_note = Note.objects.get(slug=self.note.slug)
        self.assertEqual(updated_note.title, form_data['title'])
        self.assertEqual(updated_note.text, form_data['text'])
        self.assertEqual(updated_note.slug, form_data['slug'])
        self.assertEqual(updated_note.author, self.note.author)

    def test_user_can_delete_own_note(self):
        initial_count = Note.objects.count()
        
        self.author_client.post(NOTE_DELETE_URL)

        self.assertEqual(Note.objects.count(), initial_count - 1)

    def test_user_cannot_edit_other_user_note(self):
        form_data = self.form_data.copy()
        form_data['slug'] = self.note.slug

        self.reader_client.post(NOTE_EDIT_URL, data=form_data)

        unchanged_note = Note.objects.get(slug=self.note.slug)
        self.assertEqual(unchanged_note.title, self.note.title)
        self.assertEqual(unchanged_note.text, self.note.text)
        self.assertEqual(unchanged_note.slug, self.note.slug)
        self.assertEqual(unchanged_note.author, self.note.author)

    def test_user_cannot_delete_other_user_note(self):
        self.reader_client.post(NOTE_DELETE_URL)

        note_in_db = Note.objects.get(id=self.note.id)
        self.assertEqual(note_in_db.title, self.note.title)
        self.assertEqual(note_in_db.text, self.note.text)
        self.assertEqual(note_in_db.slug, self.note.slug)
        self.assertEqual(note_in_db.author, self.note.author)
