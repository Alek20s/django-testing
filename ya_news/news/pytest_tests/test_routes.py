import pytest
from http import HTTPStatus
from django.urls import reverse


@pytest.mark.django_db
def test_home_page(client):
    url = reverse('news:home')
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK