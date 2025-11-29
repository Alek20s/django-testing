import pytest
from http import HTTPStatus
from django.urls import reverse
from news.models import News


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