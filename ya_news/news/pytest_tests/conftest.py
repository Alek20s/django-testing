import pytest

from django.contrib.auth.models import User
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
    from django.test import Client
    client = Client()
    client.force_login(author_user)
    return client


@pytest.fixture
def not_author_client(not_author_user):
    """Возвращает клиента, залогиненного как не-автор."""
    from django.test import Client
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
def multiple_news(db):
    """Создаёт много новостей для проверки пагинации."""
    from django.conf import settings
    news_list = []
    for i in range(settings.NEWS_COUNT_ON_HOME_PAGE + 5):
        news_list.append(
            News.objects.create(title=f'Новость {i}', text='Текст новости')
        )
    return news_list


@pytest.fixture
def news_with_dates(db):
    """Создаёт три новости с разными датами для проверки сортировки."""
    from datetime import datetime, timedelta
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
    return [news3, news2, news1]  # В порядке от новых к старым


@pytest.fixture
def comments_with_dates(db, author_user, news):
    """Создаёт два комментария с разными датами для проверки сортировки."""
    from datetime import datetime, timedelta
    
    old_time = datetime.now() - timedelta(days=1)
    new_time = datetime.now()
    
    comment_old = Comment.objects.create(
        news=news,
        author=author_user,
        text='Old comment',
        created=old_time
    )
    
    comment_new = Comment.objects.create(
        news=news,
        author=author_user,
        text='New comment',
        created=new_time
    )
    
    return [comment_old, comment_new]  # В хронологическом порядке
