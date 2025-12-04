from datetime import datetime, timedelta

import pytest
from django.conf import settings
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse

from news.models import Comment, News


@pytest.fixture
def author_user(db):
    """Создаёт пользователя-автора."""
    return User.objects.create_user(username='alex', password='123')


@pytest.fixture
def not_author_user(db):
    """Создаёт второго пользователя (для тестов чужих комментариев)."""
    return User.objects.create_user(username='kate', password='123')


@pytest.fixture
def news(db):
    """Создаёт новость для тестов."""
    return News.objects.create(title='Test news', text='Some text')


@pytest.fixture
def auth_client(author_user):
    """Возвращает клиента, залогиненного как автор."""
    client = Client()
    client.force_login(author_user)
    return client


@pytest.fixture
def not_author_client(not_author_user):
    """Возвращает клиента, залогиненного как не-автор."""
    client = Client()
    client.force_login(not_author_user)
    return client


@pytest.fixture
def comment(db, author_user, news):
    """Создаёт комментарий автора к новости."""
    return Comment.objects.create(
        news=news,
        author=author_user,
        text='Author comment'
    )


@pytest.fixture
def home_url():
    """URL главной страницы."""
    return reverse('news:home')


@pytest.fixture
def detail_url(news):
    """URL страницы отдельной новости."""
    return reverse('news:detail', args=[news.id])


@pytest.fixture
def edit_url(comment):
    """URL редактирования комментария."""
    return reverse('news:edit', args=[comment.id])


@pytest.fixture
def delete_url(comment):
    """URL удаления комментария."""
    return reverse('news:delete', args=[comment.id])


@pytest.fixture
def logout_url():
    """URL выхода из системы."""
    return reverse('users:logout')


@pytest.fixture
def login_url():
    """URL страницы логина."""
    return reverse('users:login')


@pytest.fixture
def multiple_news(db):
    """Создаёт новости для проверки пагинации."""
    now = datetime.now()
    return [
        News.objects.create(
            title=f'Новость {i}',
            text='Текст новости',
            date=now - timedelta(days=i)
        )
        for i in range(settings.NEWS_COUNT_ON_HOME_PAGE + 5)
    ]


@pytest.fixture
def news_with_dates(db):
    """Создаёт три новости с разными датами для проверки сортировки."""
    now = datetime.now()
    return [
        News.objects.create(
            title=f'Новость {i}',
            text='Текст новости',
            date=now - timedelta(days=i)
        )
        for i in range(3)
    ]


@pytest.fixture
def comments_with_dates(db, author_user, news):
    """Создаёт 222 комментария с разными датами для проверки сортировки."""
    now = datetime.now()
    return [
        Comment.objects.create(
            news=news,
            author=author_user,
            text=f'Comment {i}',
            created=now - timedelta(days=221 - i)
        )
        for i in range(222)
    ]
