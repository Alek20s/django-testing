from datetime import datetime, timedelta

import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from news.models import Comment, News


@pytest.mark.django_db
def test_home_page_contains_no_more_than_10_news(client):
    # создаём 15 новостей
    for i in range(15):
        News.objects.create(title=f'Новость {i}', text='Текст новости')

    url = reverse('news:home')
    response = client.get(url)
    object_list = response.context['object_list']

    # проверяем, что новостей не больше 10
    assert len(object_list) <= 10


@pytest.mark.django_db
def test_news_are_sorted_by_date(client):
    # Создаём три новости с разными датами
    now = datetime.now()

    news1 = News.objects.create(
        title='news1',
        text='text1',
        date=now - timedelta(days=2)
    )
    news2 = News.objects.create(
        title='news2',
        text='text2',
        date=now - timedelta(days=1)
    )
    news3 = News.objects.create(
        title='news3',
        text='text3',
        date=now
    )

    url = reverse('news:home')
    response = client.get(url)

    object_list = list(response.context['object_list'])

    # Проверяем порядок: сначала news3, потом news2, потом news1
    assert object_list == [news3, news2, news1]


@pytest.mark.django_db
def test_comments_are_sorted_chronologically(client):
    user = User.objects.create_user(username='alex', password='123')
    news = News.objects.create(title='Test news', text='Some text')

    old_time = datetime.now() - timedelta(days=1)
    new_time = datetime.now()

    comment_old = Comment.objects.create(
        news=news,
        author=user,
        text='Old comment',
        created=old_time
    )

    comment_new = Comment.objects.create(
        news=news,
        author=user,
        text='New comment',
        created=new_time
    )

    url = reverse('news:detail', args=[news.id])
    response = client.get(url)

    # читаем комментарии правильно: только через news
    comments = list(response.context['news'].comment_set.all())

    assert comments == [comment_old, comment_new]


@pytest.mark.django_db
def test_comment_form_availability(client):
    """
    Анонимному пользователю недоступна форма для отправки комментария
    на странице отдельной новости, а авторизованному доступна.
    """
    from news.forms import CommentForm

    news = News.objects.create(title='Test', text='Test text')
    url = reverse('news:detail', args=(news.id,))
    # Проверка для анонимного пользователя
    response = client.get(url)
    assert 'form' not in response.context
    # Проверка для авторизованного пользователя
    user = User.objects.create_user(username='testuser', password='pass')
    client.force_login(user)
    response = client.get(url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)
