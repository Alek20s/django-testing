import pytest
from django.contrib.auth.models import User
from news.models import Comment, News


@pytest.fixture
def author_user(db):
    """Создаёт пользователя-автора."""
    return User.objects.create_user(username='alex', password='123')


@pytest.fixture
def another_user(db):
    """Создаёт второго пользователя (для тестов чужих комментариев)."""
    return User.objects.create_user(username='kate', password='123')


@pytest.fixture
def news(db):
    """Создаёт новость для тестов."""
    return News.objects.create(title='Test news', text='Some text')


@pytest.fixture
def auth_client(client, author_user):
    """Возвращает клиента, залогиненного как автор."""
    client.login(username='alex', password='123')
    return client


@pytest.fixture
def comment(db, author_user, news):
    """Создаёт комментарий автора к новости."""
    return Comment.objects.create(
        news=news,
        author=author_user,
        text='Author comment'
    )