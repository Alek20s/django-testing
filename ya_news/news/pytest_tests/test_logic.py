from http import HTTPStatus

import pytest

from news.forms import BAD_WORDS
from news.models import Comment

pytestmark = pytest.mark.django_db

# Form data constants
FORM_DATA = {'text': 'Test comment'}
BAD_WORDS_DATA = [{'text': f'This is {word} word'} for word in BAD_WORDS]


def test_authenticated_user_can_add_comment(
    auth_client, author_user, news, detail_url
):
    auth_client.post(detail_url, FORM_DATA)

    # Проверяем, что комментарий создан с правильными полями
    assert Comment.objects.count() == 1
    comment = Comment.objects.get()
    assert comment.text == FORM_DATA['text']
    assert comment.news == news
    assert comment.author == author_user


def test_anonymous_user_cannot_add_comment(client, news, detail_url):
    # аноним должен быть перенаправлен на страницу логина
    assert client.post(detail_url, FORM_DATA).status_code == HTTPStatus.FOUND
    # Проверяем, что комментарий НЕ создан
    assert Comment.objects.count() == 0


@pytest.mark.parametrize('bad_word_data', BAD_WORDS_DATA)
def test_comment_with_forbidden_words_not_published(
    auth_client, news, detail_url, bad_word_data
):
    response = auth_client.post(detail_url, bad_word_data)

    # комментарий НЕ должен создаться
    assert Comment.objects.count() == 0

    # форма должна содержать ошибку
    assert response.context['form'].errors


def test_author_can_edit_own_comment(
    auth_client, comment, edit_url
):
    """Авторизованный пользователь может редактировать комментарии."""
    response = auth_client.post(edit_url, FORM_DATA)
    assert response.status_code == HTTPStatus.FOUND

    # Read fresh from database and check text field
    updated_comment = Comment.objects.get(pk=comment.pk)
    assert updated_comment.text == FORM_DATA['text']
    assert updated_comment.author == comment.author
    assert updated_comment.news == comment.news


def test_author_can_delete_own_comment(auth_client, comment, delete_url):
    """Авторизованный пользователь может удалить свой комментарий."""
    response = auth_client.post(delete_url)
    assert response.status_code == HTTPStatus.FOUND

    # Проверяем, что комментарий удален из базы
    assert Comment.objects.count() == 0


def test_not_author_cannot_edit_comment(
    not_author_client, comment, edit_url
):
    """Не-автор не может редактировать чужой комментарий."""
    original_text = comment.text
    response = not_author_client.post(edit_url, FORM_DATA)
    assert response.status_code == HTTPStatus.NOT_FOUND

    # Проверяем, что комментарий НЕ изменился
    comment_from_db = Comment.objects.get(pk=comment.pk)
    assert comment_from_db.text == original_text
    assert comment_from_db.author == comment.author
    assert comment_from_db.news == comment.news


def test_not_author_cannot_delete_comment(
    not_author_client, comment, delete_url
):
    """Не-автор не может удалить чужой комментарий."""
    response = not_author_client.post(delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND

    # Проверяем, что комментарий НЕ удален
    assert Comment.objects.count() == 1
    comment_from_db = Comment.objects.get(pk=comment.pk)
    assert comment_from_db.text == comment.text
    assert comment_from_db.author == comment.author
    assert comment_from_db.news == comment.news
