from django.db import models
from books.models import Book
from authors.models import Author


class View(models.Model):
    """Модель просмотров книг"""
    book = models.ForeignKey(Book, related_name="view", on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(Author, related_name="view", on_delete=models.CASCADE, null=True)
    views = models.PositiveIntegerField(verbose_name='Количество просмотров', default=1, null=True)
    date = models.DateField(verbose_name="Дата просмотров", auto_now_add=True)

    class Meta:
        ordering = ['-views']
        verbose_name = 'Просмотры'
        verbose_name_plural = 'Просмотры'