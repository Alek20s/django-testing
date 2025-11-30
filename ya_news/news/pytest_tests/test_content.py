import pytest
from django.urls import reverse
from news.models import News


@pytest.mark.django_db
def test_home_page_contains_no_more_than_10_news(client):
    # создаём 15 новостей
    for i in range(15):
        News.objects.create(title=f'Новость {i}', text='Текст новости')
    
    url = reverse('news:home')  # замени на нужное имя маршрута, если отличается
    response = client.get(url)
    object_list = response.context['object_list']

    # проверяем, что новостей не больше 10
    assert len(object_list) <= 10
