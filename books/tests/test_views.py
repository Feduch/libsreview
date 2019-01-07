from django.test import TestCase
from django.urls import reverse
from books.models import Book


class BooksListViewTest(TestCase):
    """Проверяет доступ к разделу книги"""
    fixtures = ['test_authors.json', 'genres.json', 'series.json', 'test_books.json']

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/book/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('books-list'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('books-list'))
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'books/book_list.html')


class BookDetailViewTest(TestCase):
    """Проверяет доступ к книге"""
    fixtures = ['test_authors.json', 'genres.json', 'series.json', 'test_books.json']

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/book/1/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        book = Book.objects.get(pk=1)
        resp = self.client.get(book.get_absolute_url())
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        book = Book.objects.get(pk=1)
        resp = self.client.get(book.get_absolute_url())
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'books/book_detail.html')