from http import HTTPStatus

import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from news.forms import BAD_WORDS
from news.models import Comment, News

pytestmark = pytest.mark.django_db

# Form data constants
COMMENT_TEXT = {'text': 'Test comment'}
ANON_COMMENT_TEXT = {'text': 'Anon comment'}
BAD_WORD_COMMENT = {'text': f'This is {BAD_WORDS[0]} word'}
UPDATED_COMMENT_TEXT = {'text': 'Updated text'}


def test_authenticated_user_can_add_comment(auth_client, author_user, news, detail_url):
    auth_client.post(detail_url, COMMENT_TEXT)
    
    # Проверяем, что комментарий создан с правильными полями
    assert Comment.objects.count() == 1
    comment = Comment.objects.get()
    assert comment.text == COMMENT_TEXT['text']
    assert comment.news == news
    assert comment.author == author_user


def test_anonymous_user_cannot_add_comment(client, news, detail_url):
    response = client.post(detail_url, ANON_COMMENT_TEXT)

    # аноним должен быть перенаправлен на страницу логина
    assert response.status_code == HTTPStatus.FOUND  # 302
    # Проверяем, что комментарий НЕ создан
    assert Comment.objects.count() == 0


def test_comment_with_forbidden_words_not_published(auth_client, news, detail_url):
    response = auth_client.post(detail_url, BAD_WORD_COMMENT)

    # комментарий НЕ должен создаться
    assert Comment.objects.count() == 0

    # форма должна содержать ошибку
    assert response.context['form'].errors


def test_author_can_edit_own_comment(auth_client, author_user, news, comment, edit_url):
    """Авторизованный пользователь может редактировать комментарии."""
    response = auth_client.post(edit_url, UPDATED_COMMENT_TEXT)
    assert response.status_code == HTTPStatus.FOUND
    
    # Read fresh from database and check all 3 fields
    updated_comment = Comment.objects.get(pk=comment.pk)
    assert updated_comment.text == UPDATED_COMMENT_TEXT['text']
    assert updated_comment.news == news
    assert updated_comment.author == author_user


def test_author_can_delete_own_comment(auth_client, comment, delete_url):
    """Авторизованный пользователь может удалить свой комментарий."""
    response = auth_client.post(delete_url)
    assert response.status_code == HTTPStatus.FOUND
    
    # Проверяем, что комментарий удален из базы
    assert Comment.objects.count() == 0
