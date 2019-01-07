from django.db import models
from django.contrib.auth.models import User


class Comment(models.Model):
    book = models.ForeignKey('books.Book', blank=True, null=True, on_delete=models.CASCADE)
    author = models.ForeignKey('authors.Author', blank=True, null=True, on_delete=models.CASCADE)
    publication = models.ForeignKey('publications.Publication', blank=True, null=True, on_delete=models.CASCADE)
    collection = models.ForeignKey('collection.Collection', blank=True, null=True, on_delete=models.CASCADE)
    date_create = models.DateTimeField("Дата публикации", auto_now_add=True)
    user = models.ForeignKey(User, verbose_name="Голос пользователя", on_delete=models.SET_NULL, null=True)
    text = models.TextField('Комментарий')

    class Meta:
        ordering = ['-id']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'