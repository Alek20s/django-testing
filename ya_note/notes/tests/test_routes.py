from http import HTTPStatus

from .test_base import (
    BaseTestCase,
    HOME_URL,
    LIST_URL,
    ADD_URL,
    SUCCESS_URL,
    LOGIN_URL,
    SIGNUP_URL,
)


class TestRoutes(BaseTestCase):

    def test_pages_availability(self):
        """Тест доступности страниц для разных пользователей."""
        urls = [
            (HOME_URL, self.client, HTTPStatus.OK),
            (LOGIN_URL, self.client, HTTPStatus.OK),
            (SIGNUP_URL, self.client, HTTPStatus.OK),
            (LIST_URL, self.author_client, HTTPStatus.OK),
            (ADD_URL, self.author_client, HTTPStatus.OK),
            (SUCCESS_URL, self.author_client, HTTPStatus.OK),
            (self.note_detail_url, self.author_client, HTTPStatus.OK),
            (self.note_edit_url, self.author_client, HTTPStatus.OK),
            (self.note_delete_url, self.author_client, HTTPStatus.OK),
            (self.note_detail_url, self.reader_client, HTTPStatus.NOT_FOUND),
            (self.note_edit_url, self.reader_client, HTTPStatus.NOT_FOUND),
            (self.note_delete_url, self.reader_client, HTTPStatus.NOT_FOUND),
        ]

        for url, client, expected_status in urls:
            with self.subTest(url=url, client=client):
                response = client.get(url)
                self.assertEqual(response.status_code, expected_status)

    def test_redirects_for_anonymous(self):
        """Тест редиректов для анонимных пользователей."""
        urls = [
            (LIST_URL, f'{LOGIN_URL}?next={LIST_URL}'),
            (ADD_URL, f'{LOGIN_URL}?next={ADD_URL}'),
            (SUCCESS_URL, f'{LOGIN_URL}?next={SUCCESS_URL}'),
            (self.note_detail_url, f'{LOGIN_URL}?next={self.note_detail_url}'),
            (self.note_edit_url, f'{LOGIN_URL}?next={self.note_edit_url}'),
            (self.note_delete_url, f'{LOGIN_URL}?next={self.note_delete_url}'),
        ]
  
        for url, expected_redirect in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertRedirects(response, expected_redirect)
