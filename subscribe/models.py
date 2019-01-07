from django.db import models


class Subscriber(models.Model):
    email = models.CharField('E-mail', max_length=255)
    book = models.ForeignKey('books.Book', blank=True, null=True, on_delete=models.CASCADE)
    author = models.ForeignKey('authors.Author', blank=True, null=True, on_delete=models.CASCADE)
    collection = models.ForeignKey('collection.Collection', blank=True, null=True, on_delete=models.CASCADE)
    date_create = models.DateTimeField("Дата подписки", auto_now_add=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Подписчики'
        verbose_name_plural = 'Подписчики'
