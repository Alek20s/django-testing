from http import HTTPStatus

from .test_base import (
    BaseTestCase,
    HOME_URL,
    LIST_URL,
    ADD_URL,
    SUCCESS_URL,
    LOGIN_URL,
    SIGNUP_URL,
    NOTE_DETAIL_URL,
    NOTE_EDIT_URL,
    NOTE_DELETE_URL,
    LIST_REDIRECT_URL,
    ADD_REDIRECT_URL,
    SUCCESS_REDIRECT_URL,
    NOTE_DETAIL_REDIRECT_URL,
    NOTE_EDIT_REDIRECT_URL,
    NOTE_DELETE_REDIRECT_URL,
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
            (NOTE_DETAIL_URL, self.author_client, HTTPStatus.OK),
            (NOTE_EDIT_URL, self.author_client, HTTPStatus.OK),
            (NOTE_DELETE_URL, self.author_client, HTTPStatus.OK),
            (NOTE_DETAIL_URL, self.reader_client, HTTPStatus.NOT_FOUND),
            (NOTE_EDIT_URL, self.reader_client, HTTPStatus.NOT_FOUND),
            (NOTE_DELETE_URL, self.reader_client, HTTPStatus.NOT_FOUND),
            (LIST_URL, self.client, HTTPStatus.FOUND),
            (ADD_URL, self.client, HTTPStatus.FOUND),
            (SUCCESS_URL, self.client, HTTPStatus.FOUND),
            (NOTE_DETAIL_URL, self.client, HTTPStatus.FOUND),
            (NOTE_EDIT_URL, self.client, HTTPStatus.FOUND),
            (NOTE_DELETE_URL, self.client, HTTPStatus.FOUND),
        ]

        for url, client, expected_status in urls:
            with self.subTest(url=url, client=client):
                self.assertEqual(client.get(url).status_code, expected_status)

    def test_redirects_for_anonymous(self):
        """Тест редиректов для анонимных пользователей."""
        urls = [
            (LIST_URL, LIST_REDIRECT_URL),
            (ADD_URL, ADD_REDIRECT_URL),
            (SUCCESS_URL, SUCCESS_REDIRECT_URL),
            (NOTE_DETAIL_URL, NOTE_DETAIL_REDIRECT_URL),
            (NOTE_EDIT_URL, NOTE_EDIT_REDIRECT_URL),
            (NOTE_DELETE_URL, NOTE_DELETE_REDIRECT_URL),
        ]

        for url, expected_redirect in urls:
            with self.subTest(url=url):
                self.assertRedirects(self.client.get(url), expected_redirect)
