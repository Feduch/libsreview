from bs4 import BeautifulSoup
from django.test import TestCase
from django.utils.html import strip_tags
from books.models import Book


class BookTestCase(TestCase):
    fixtures = ['test_authors.json', 'genres.json', 'series.json', 'test_books.json']

    def test_book_seo(self):
        """Парсит страницу и проверяет seo теги"""
        # Книга с одним автором
        book_one_author = Book.objects.get(pk=1)
        title = "{0} (скачать fb2), {1}".format(book_one_author.title, book_one_author.get_authors())
        description = "{0}...".format(strip_tags(book_one_author.description)[:197])
        keywords = "{0}, {1}, скачать fb2".format(book_one_author.title, book_one_author.get_authors())
        resp = self.client.get(book_one_author.get_absolute_url())
        soup = BeautifulSoup(resp.content, 'html.parser')
        client_description = soup.findAll(attrs={"name":"description"})
        client_keywords = soup.findAll(attrs={"name":"keywords"})
        self.assertEqual(title, soup.title.string)
        self.assertEqual(description, client_description[0]['content'])
        self.assertEqual(keywords, client_keywords[0]['content'])

        # Книга с несколькими авторами
        book_any_author = Book.objects.get(pk=2)
        title = "{0} (скачать fb2), {1}".format(book_any_author.title, book_any_author.get_authors())
        description = "{0}...".format(strip_tags(book_any_author.description)[:197])
        keywords = "{0}, {1}, скачать fb2".format(book_any_author.title, book_any_author.get_authors())
        resp = self.client.get(book_any_author.get_absolute_url())
        soup = BeautifulSoup(resp.content, 'html.parser')
        client_description = soup.findAll(attrs={"name": "description"})
        client_keywords = soup.findAll(attrs={"name": "keywords"})
        self.assertEqual(title, soup.title.string)
        self.assertEqual(description, client_description[0]['content'])
        self.assertEqual(keywords, client_keywords[0]['content'])