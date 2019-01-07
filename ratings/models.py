from django.db import models
from django.contrib.auth.models import User


class StarRatings(models.Model):
    book = models.ForeignKey('books.Book', blank=True, null=True, on_delete=models.CASCADE)
    author = models.ForeignKey('authors.Author', blank=True, null=True, on_delete=models.CASCADE)
    publication = models.ForeignKey('publications.Publication', blank=True, null=True, on_delete=models.CASCADE)
    collection = models.ForeignKey('collection.Collection', blank=True, null=True, on_delete=models.CASCADE)
    rating = models.DecimalField('Количество звезд', default=0, max_digits=3, decimal_places=2)
    date_create = models.DateTimeField("Дата голоса", auto_now_add=True)
    user = models.ForeignKey(User, verbose_name="Голос пользователя", on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'Оценку'
        verbose_name_plural = 'Оценки'