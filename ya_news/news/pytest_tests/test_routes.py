from http import HTTPStatus

import pytest
from pytest_lazy_fixtures import lf

pytestmark = pytest.mark.django_db

# HTTP Status constants
OK = HTTPStatus.OK
FOUND = HTTPStatus.FOUND
NOT_FOUND = HTTPStatus.NOT_FOUND

# HTTP Method constants
GET = 'get'
POST = 'post'


@pytest.mark.parametrize(
    'test_client, test_url, method, expected_status',
    [
        (lf('client'), lf('home_url'), GET, OK),
        (lf('client'), lf('detail_url'), GET, OK),
        (lf('auth_client'), lf('edit_url'), GET, OK),
        (lf('auth_client'), lf('delete_url'), GET, OK),
        (lf('not_author_client'), lf('edit_url'), GET, NOT_FOUND),
        (lf('not_author_client'), lf('delete_url'), GET, NOT_FOUND),
        (lf('client'), lf('logout_url'), POST, OK),
    ]
)
def test_pages_availability(test_client, test_url, method, expected_status):
    """Проверка доступности страниц для разных пользователей."""
    if method == POST:
        response = test_client.post(test_url)
    else:
        response = test_client.get(test_url)

    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'test_url, redirect_url',
    [
        (lf('edit_url'), lf('edit_redirect_url')),
        (lf('delete_url'), lf('delete_redirect_url')),
    ]
)
def test_redirect_to_login(client, test_url, redirect_url):
    """Проверка редиректа на страницу логина для анонимных пользователей."""
    response = client.get(test_url)
    
    assert response.status_code == FOUND
    assert response.url == redirect_url
