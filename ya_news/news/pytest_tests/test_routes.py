from http import HTTPStatus

import pytest

pytestmark = pytest.mark.django_db

# HTTP Status constants
OK = HTTPStatus.OK
FOUND = HTTPStatus.FOUND
NOT_FOUND = HTTPStatus.NOT_FOUND


@pytest.mark.parametrize(
    'client_name, url_name, method, expected_status, redirect_to_login',
    [
        ('client', 'home_url', 'get', OK, False),
        ('client', 'detail_url', 'get', OK, False),
        ('auth_client', 'edit_url', 'get', OK, False),
        ('auth_client', 'delete_url', 'get', OK, False),
        ('not_author_client', 'edit_url', 'get', NOT_FOUND, False),
        ('not_author_client', 'delete_url', 'get', NOT_FOUND, False),
        ('client', 'logout_url', 'post', OK, False),
        ('client', 'edit_url', 'get', FOUND, True),
        ('client', 'delete_url', 'get', FOUND, True),
    ]
)
def test_pages_availability(
    request, client_name, url_name, method, expected_status, redirect_to_login, login_url
):
    """Проверка доступности страниц для разных пользователей."""
    client_fixture = request.getfixturevalue(client_name)
    url_fixture = request.getfixturevalue(url_name)

    if method == 'post':
        response = client_fixture.post(url_fixture)
    else:
        response = client_fixture.get(url_fixture)

    assert response.status_code == expected_status

    if redirect_to_login:
        expected_redirect = f'{login_url}?next={url_fixture}'
        assert response.url == expected_redirect
