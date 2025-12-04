import pytest
from django.conf import settings

from news.forms import CommentForm

pytestmark = pytest.mark.django_db


def test_home_page_contains_no_more_than_10_news(
    client, multiple_news, home_url
):
    """Проверка количества новостей на главной странице."""
    response = client.get(home_url)
    object_list = response.context['object_list']

    assert len(object_list) == settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_are_sorted_by_date(client, news_with_dates, home_url):
    """Проверка сортировки новостей от новых к старым."""
    response = client.get(home_url)

    object_list = list(response.context['object_list'])

    # Проверяем порядок: сначала news3, потом news2, потом news1
    assert object_list == news_with_dates

    # Проверяем, что новости отсортированы по дате от новых к старым
    all_dates = [news.date for news in object_list]
    assert all_dates == sorted(all_dates, reverse=True)


def test_comments_are_sorted_chronologically(
    client, comments_with_dates, detail_url
):
    """Проверка хронологической сортировки комментариев."""
    response = client.get(detail_url)

    # читаем комментарии правильно: только через news
    comments = list(response.context['news'].comment_set.all())

    assert comments == comments_with_dates

    # Проверяем, что комментарии отсортированы хронологически
    # (от старых к новым)
    all_dates = [comment.created for comment in comments]
    assert all_dates == sorted(all_dates)


def test_anonymous_user_no_form(client, news, detail_url):
    """Анонимному пользователю недоступна форма для комментария."""
    response = client.get(detail_url)
    assert 'form' not in response.context


def test_authenticated_user_has_form(auth_client, news, detail_url):
    """Авторизованному пользователю доступна форма для комментария."""
    response = auth_client.get(detail_url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)
