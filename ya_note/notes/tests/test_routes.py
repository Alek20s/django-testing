from http import HTTPStatus
from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class TestRoutes(TestCase):
    def test_home_page_available_to_anonymous(self):
        client = Client()
        url = reverse('notes:home')  # замените на имя маршрута главной страницы, если другое
        response = client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)


class TestRoutes(TestCase):
    def test_home_page_available_to_anonymous(self):
        client = Client()
        url = reverse('notes:home')  # замени на актуальное имя маршрута
        response = client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_notes_page_available_to_authenticated_user(self):
        user = User.objects.create_user(username='alex', password='pass123')
        client = Client()
        client.login(username='alex', password='pass123')
        url = reverse('notes:list')  # замени на актуальное имя маршрута
        response = client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
