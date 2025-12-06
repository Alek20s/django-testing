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


@pytest.mark.parametrize(
    'client_name, url_name, method, expected_status',
    [
        (pytest.lazy_fixture('client'), pytest.lazy_fixture('home_url'), GET, OK),
        (pytest.lazy_fixture('client'), pytest.lazy_fixture('detail_url'), GET, OK),
        (pytest.lazy_fixture('auth_client'), pytest.lazy_fixture('edit_url'), GET, OK),
        (pytest.lazy_fixture('auth_client'), pytest.lazy_fixture('delete_url'), GET, OK),
        (pytest.lazy_fixture('not_author_client'), pytest.lazy_fixture('edit_url'), GET, NOT_FOUND),
        (pytest.lazy_fixture('not_author_client'), pytest.lazy_fixture('delete_url'), GET, NOT_FOUND),
        (pytest.lazy_fixture('client'), pytest.lazy_fixture('logout_url'), POST, OK),
        # случаи перенаправления для анонимного клиента
        (pytest.lazy_fixture('client'), pytest.lazy_fixture('edit_url'), GET, FOUND),
        (pytest.lazy_fixture('client'), pytest.lazy_fixture('delete_url'), GET, FOUND),
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
        (pytest.lazy_fixture('edit_url'), pytest.lazy_fixture('edit_redirect_url')),
        (pytest.lazy_fixture('delete_url'), pytest.lazy_fixture('delete_redirect_url')),
    ]
)
def test_redirect_to_login(client, url_name, redirect_url_name):
    """Проверка редиректа на страницу логина для анонимных пользователей."""
    response = client.get(url_name)
    assert response.url == redirect_url_name
