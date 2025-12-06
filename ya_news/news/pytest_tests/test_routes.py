from http import HTTPStatus
import pytest

pytestmark = pytest.mark.django_db

# HTTP Status constants
OK = HTTPStatus.OK
FOUND = HTTPStatus.FOUND
NOT_FOUND = HTTPStatus.NOT_FOUND

# HTTP Method constants
GET = 'get'
POST = 'post'

# Fixtures as constants
CLIENT = pytest.lazy_fixture('client')
AUTH_CLIENT = pytest.lazy_fixture('auth_client')
NOT_AUTHOR_CLIENT = pytest.lazy_fixture('not_author_client')

HOME_URL = pytest.lazy_fixture('home_url')
DETAIL_URL = pytest.lazy_fixture('detail_url')
EDIT_URL = pytest.lazy_fixture('edit_url')
DELETE_URL = pytest.lazy_fixture('delete_url')
LOGOUT_URL = pytest.lazy_fixture('logout_url')

EDIT_REDIRECT_URL = pytest.lazy_fixture('edit_redirect_url')
DELETE_REDIRECT_URL = pytest.lazy_fixture('delete_redirect_url')


@pytest.mark.parametrize(
    'client_name, url_name, method, expected_status',
    [
        (CLIENT, HOME_URL, GET, OK),
        (CLIENT, DETAIL_URL, GET, OK),
        (AUTH_CLIENT, EDIT_URL, GET, OK),
        (AUTH_CLIENT, DELETE_URL, GET, OK),
        (NOT_AUTHOR_CLIENT, EDIT_URL, GET, NOT_FOUND),
        (NOT_AUTHOR_CLIENT, DELETE_URL, GET, NOT_FOUND),
        (CLIENT, LOGOUT_URL, POST, OK),
        # случаи перенаправления для анонимного клиента
        (CLIENT, EDIT_URL, GET, FOUND),
        (CLIENT, DELETE_URL, GET, FOUND),
    ]
)
def test_pages_availability(client_name, url_name, method, expected_status):
    """Проверка доступности страниц для разных пользователей."""
    client = client_name
    url = url_name

    if method == POST:
        response = client.post(url)
    else:
        response = client.get(url)

    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'url_name, redirect_url_name',
    [
        (EDIT_URL, EDIT_REDIRECT_URL),
        (DELETE_URL, DELETE_REDIRECT_URL),
    ]
)
def test_redirect_to_login(client, url_name, redirect_url_name):
    """Проверка редиректа на страницу логина для анонимных пользователей."""
    response = client.get(url_name)
    assert response.url == redirect_url_name
