import pytest
from django.urls import reverse
from news.models import News, Comment
from django.contrib.auth.models import User


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
