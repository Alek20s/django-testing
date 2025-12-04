from http import HTTPStatus

import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'client_name, url_name, method, expected_status',
    [
        ('client', 'home_url', 'get', HTTPStatus.OK),
        ('client', 'detail_url', 'get', HTTPStatus.OK),
        ('auth_client', 'edit_url', 'get', HTTPStatus.OK),
        ('auth_client', 'delete_url', 'get', HTTPStatus.OK),
        ('not_author_client', 'edit_url', 'get', HTTPStatus.NOT_FOUND),
        ('not_author_client', 'delete_url', 'get', HTTPStatus.NOT_FOUND),
        ('client', 'logout_url', 'post', HTTPStatus.OK),
    ]
)
def test_pages_availability(
    request, client_name, url_name, method, expected_status
):
    """Проверка доступности страниц для разных пользователей."""
    client_fixture = request.getfixturevalue(client_name)
    url_fixture = request.getfixturevalue(url_name)

    if method == 'post':
        response = client_fixture.post(url_fixture)
    else:
        response = client_fixture.get(url_fixture)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'url_name',
    ['edit_url', 'delete_url']
)
def test_redirects(client, request, url_name):
    """Проверка перенаправлений для неавторизованных пользователей."""
    url_fixture = request.getfixturevalue(url_name)
    response = client.get(url_fixture)
    assert response.status_code == HTTPStatus.FOUND
    # Проверяем, что перенаправление идет на страницу логина
    login_url = reverse('users:login')
    assert response.url.startswith(login_url)
