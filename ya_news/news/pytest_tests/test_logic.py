import pytest
from django.urls import reverse
from news.models import News, Comment
from django.contrib.auth.models import User
from http import HTTPStatus



@pytest.mark.django_db
def test_authenticated_user_can_add_comment(client):
    user = User.objects.create_user(username='alex', password='123')
    news = News.objects.create(title='Test news', text='Some text')
    client.login(username='alex', password='123')

    url = reverse('news:detail', args=[news.id])
    data = {'text': 'Test comment'}
    client.post(url, data)

    # просто проверяем, что появился хотя бы один комментарий
    assert Comment.objects.count() == 1


@pytest.mark.django_db
def test_anonymous_user_cannot_add_comment(client):
    news = News.objects.create(title='Test news', text='Some text')

    url = reverse('news:detail', args=[news.id])
    data = {'text': 'Anon comment'}

    response = client.post(url, data)

    # аноним должен быть перенаправлен на страницу логина
    assert response.status_code == HTTPStatus.FOUND  # 302


@pytest.mark.django_db
def test_comment_with_forbidden_words_not_published(client):
    user = User.objects.create_user(username='alex', password='123')
    client.login(username='alex', password='123')

    news = News.objects.create(title='Test news', text='Some text')

    url = reverse('news:detail', args=[news.id])

    # одно из запрещённых слов — "редиска"
    data = {'text': 'This is редиска word'}

    response = client.post(url, data)

    # комментарий НЕ должен создаться
    assert Comment.objects.count() == 0

    # форма должна содержать ошибку
    assert response.context['form'].errors

