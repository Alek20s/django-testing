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
        ('client', 'home_url', GET, OK),
        ('client', 'detail_url', GET, OK),
        ('auth_client', 'edit_url', GET, OK),
        ('auth_client', 'delete_url', GET, OK),
        ('not_author_client', 'edit_url', GET, NOT_FOUND),
        ('not_author_client', 'delete_url', GET, NOT_FOUND),
        ('client', 'logout_url', POST, OK),
    ]
)
def test_pages_availability(
    request, client_name, url_name, method, expected_status
):
    """Проверка доступности страниц для разных пользователей."""
    client_fixture = request.getfixturevalue(client_name)
    url_fixture = request.getfixturevalue(url_name)

    if method == POST:
        response = client_fixture.post(url_fixture)
    else:
        response = client_fixture.get(url_fixture)

    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'url_name, redirect_url_name',
    [
        ('edit_url', 'edit_redirect_url'),
        ('delete_url', 'delete_redirect_url'),
    ]
)
def test_redirect_to_login(request, client, url_name, redirect_url_name):
    """Проверка редиректа на страницу логина для анонимных пользователей."""
    url_fixture = request.getfixturevalue(url_name)
    redirect_url_fixture = request.getfixturevalue(redirect_url_name)
    
    response = client.get(url_fixture)
    
    assert response.status_code == FOUND
    assert response.url == redirect_url_fixture
