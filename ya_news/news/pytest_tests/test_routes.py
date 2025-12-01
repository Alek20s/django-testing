import pytest
from http import HTTPStatus
from django.urls import reverse
from news.models import News
from django.contrib.auth.models import User
from news.models import Comment


@pytest.mark.django_db
def test_home_page(client):
    url = reverse('news:home')
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_news_detail_page(client):
    news = News.objects.create(title='Test', text='Test text')
    url = reverse('news:detail', args=[news.id])
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_comment_edit_available_to_author(client):
    from django.contrib.auth.models import User
    from news.models import Comment   
    author = User.objects.create_user(username='author', password='pass')
    client.login(username='author', password='pass')
    news = News.objects.create(title='Test', text='Test text')
    comment = Comment.objects.create(news=news, author=author, text='Comment')   
    url = reverse('news:edit', args=[comment.id])
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_comment_delete_available_to_author(client):
    from django.contrib.auth.models import User
    from news.models import Comment   
    author = User.objects.create_user(username='author', password='pass')
    client.login(username='author', password='pass')
    news = News.objects.create(title='Test', text='Test text')
    comment = Comment.objects.create(news=news, author=author, text='Comment')   
    url = reverse('news:delete', args=[comment.id])
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_anonymous_user_redirected_from_comment_edit(client):
    author = User.objects.create_user(username='author', password='pass')
    news = News.objects.create(title='Test', text='Test text')
    comment = Comment.objects.create(news=news, author=author, text='Comment')
    url = reverse('news:edit', args=[comment.id])
    response = client.get(url)
    # анонимный пользователь должен быть перенаправлен на страницу логина
    assert response.status_code == HTTPStatus.FOUND  # 302


@pytest.mark.django_db
def test_user_cannot_edit_other_users_comment(client):
    # Автор комментария
    author = User.objects.create_user(username='author', password='pass')
    # Другой пользователь
    other_user = User.objects.create_user(username='other', password='pass')
    # Комментарий, который принадлежит author
    news = News.objects.create(title='Test', text='Text')
    comment = Comment.objects.create(news=news, author=author, text='Comment')
    # Логинимся под "other"
    client.login(username='other', password='pass')
    # Пытаемся редактировать чужой комментарий
    url = reverse('news:edit', args=[comment.id])
    response = client.get(url)
    # Должно быть "страница не найдена"
    assert response.status_code == HTTPStatus.NOT_FOUND  # 404


@pytest.mark.django_db
def test_user_cannot_delete_other_users_comment(client):
    # Автор комментария
    author = User.objects.create_user(username='author', password='pass')

    # Другой пользователь
    other_user = User.objects.create_user(username='other', password='pass')

    # Комментарий автора
    news = News.objects.create(title='Test', text='Text')
    comment = Comment.objects.create(news=news, author=author, text='Comment')

    # Логинимся под "other"
    client.login(username='other', password='pass')

    # Пытаемся удалить чужой комментарий
    url = reverse('news:delete', args=[comment.id])
    response = client.get(url)

    # Должно быть 404
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.django_db
def test_logout_page_available_to_anonymous(client):
    """Страница выхода доступна анонимному пользователю."""
    url = reverse('users:logout')
    response = client.post(url)
    assert response.status_code == HTTPStatus.OK
