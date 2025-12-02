from http import HTTPStatus
from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class TestRoutes(TestCase):
    def test_home_page_available_to_anonymous(self):
        client = Client()
        # замените на имя маршрута главной страницы, если другое
        url = reverse('notes:home')
        response = client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)


class TestRoutes(TestCase):
    def test_home_page_available_to_anonymous(self):
        client = Client()
        url = reverse('notes:home')  # замени на актуальное имя маршрута
        response = client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_notes_page_available_to_authenticated_user(self):
        User.objects.create_user(username='alex', password='pass123')
        client = Client()
        client.login(username='alex', password='pass123')
        url = reverse('notes:list')  # замени на актуальное имя маршрута
        response = client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_done_page_available_to_authenticated_user(self):
        User.objects.create_user(username='alex', password='pass123')
        client = Client()
        client.login(username='alex', password='pass123')
        url = reverse('notes:success')
        response = client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_add_page_available_to_authenticated_user(self):
        User.objects.create_user(username='alex', password='pass123')
        client = Client()
        client.login(username='alex', password='pass123')
        url = reverse('notes:add')
        response = client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_author_can_access_note_detail(self):
        from notes.models import Note
        user = User.objects.create_user(username='author', password='pass123')
        client = Client()
        client.login(username='author', password='pass123')
        note = Note.objects.create(
            title='Test',
            text='Text',
            slug='test-slug',
            author=user
        )
        url = reverse('notes:detail', args=[note.slug])
        response = client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_author_can_access_note_edit(self):
        from notes.models import Note
        user = User.objects.create_user(username='author', password='pass123')
        client = Client()
        client.login(username='author', password='pass123')
        note = Note.objects.create(
            title='Test',
            text='Text',
            slug='test-slug',
            author=user
        )
        url = reverse('notes:edit', args=[note.slug])
        response = client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_author_can_access_note_delete(self):
        from notes.models import Note
        user = User.objects.create_user(username='author', password='pass123')
        client = Client()
        client.login(username='author', password='pass123')
        note = Note.objects.create(
            title='Test',
            text='Text',
            slug='test-slug',
            author=user
        )
        url = reverse('notes:delete', args=[note.slug])
        response = client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_other_user_gets_404_for_note_detail(self):
        from notes.models import Note
        author = User.objects.create_user(
            username='author',
            password='pass123'
        )
        User.objects.create_user(username='other', password='pass123')
        note = Note.objects.create(
            title='Test',
            text='Text',
            slug='test-slug',
            author=author
        )
        client = Client()
        client.login(username='other', password='pass123')
        url = reverse('notes:detail', args=[note.slug])
        response = client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_other_user_gets_404_for_note_edit(self):
        from notes.models import Note
        author = User.objects.create_user(
            username='author',
            password='pass123'
        )
        User.objects.create_user(username='other', password='pass123')
        note = Note.objects.create(
            title='Test',
            text='Text',
            slug='test-slug',
            author=author
        )
        client = Client()
        client.login(username='other', password='pass123')
        url = reverse('notes:edit', args=[note.slug])
        response = client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_other_user_gets_404_for_note_delete(self):
        from notes.models import Note
        author = User.objects.create_user(
            username='author',
            password='pass123'
        )
        User.objects.create_user(username='other', password='pass123')
        note = Note.objects.create(
            title='Test',
            text='Text',
            slug='test-slug',
            author=author
        )
        client = Client()
        client.login(username='other', password='pass123')
        url = reverse('notes:delete', args=[note.slug])
        response = client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_anonymous_redirected_to_login_for_notes_list(self):
        client = Client()
        url = reverse('notes:list')
        login_url = reverse('users:login')
        response = client.get(url)
        self.assertRedirects(response, f'{login_url}?next={url}')

    def test_anonymous_redirected_to_login_for_done_page(self):
        client = Client()
        url = reverse('notes:success')
        login_url = reverse('users:login')
        response = client.get(url)
        self.assertRedirects(response, f'{login_url}?next={url}')

    def test_anonymous_redirected_to_login_for_add_page(self):
        client = Client()
        url = reverse('notes:add')
        login_url = reverse('users:login')
        response = client.get(url)
        self.assertRedirects(response, f'{login_url}?next={url}')

    def test_anonymous_redirected_to_login_for_note_detail(self):
        from notes.models import Note
        user = User.objects.create_user(username='author', password='pass123')
        note = Note.objects.create(
            title='Test',
            text='Text',
            slug='test-slug',
            author=user
        )
        client = Client()
        url = reverse('notes:detail', args=[note.slug])
        login_url = reverse('users:login')
        response = client.get(url)
        self.assertRedirects(response, f'{login_url}?next={url}')

    def test_anonymous_redirected_to_login_for_note_edit(self):
        from notes.models import Note
        user = User.objects.create_user(username='author', password='pass123')
        note = Note.objects.create(
            title='Test',
            text='Text',
            slug='test-slug',
            author=user
        )
        client = Client()
        url = reverse('notes:edit', args=[note.slug])
        login_url = reverse('users:login')
        response = client.get(url)
        self.assertRedirects(response, f'{login_url}?next={url}')

    def test_anonymous_redirected_to_login_for_note_delete(self):
        from notes.models import Note
        user = User.objects.create_user(username='author', password='pass123')
        note = Note.objects.create(
            title='Test',
            text='Text',
            slug='test-slug',
            author=user
        )
        client = Client()
        url = reverse('notes:delete', args=[note.slug])
        login_url = reverse('users:login')
        response = client.get(url)
        self.assertRedirects(response, f'{login_url}?next={url}')

    def test_signup_page_available_to_all(self):
        client = Client()
        url = reverse('users:signup')
        response = client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_login_page_available_to_all(self):
        client = Client()
        url = reverse('users:login')
        response = client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
