from django.utils.text import Truncator
from django.db import models
from django.contrib.auth.models import User
from authors.models import Author
from books.models import Book
from series.models import Series


def publication_image_path(instance, filename):
    return 'publications/{0}/{1}'.format(instance.id, filename)


class Publication(models.Model):
    title = models.CharField(verbose_name='Название поста', max_length=255)
    preview_text = models.TextField(verbose_name='Краткое описание')
    detail_text = models.TextField(verbose_name='Текст')
    image = models.ImageField(verbose_name='Обложка', upload_to=publication_image_path, blank=True, null=True)
    rating = models.DecimalField('Рейтинг', default=0, max_digits=3, decimal_places=2)
    age = models.PositiveIntegerField(verbose_name='Возрасное ограничение', default=0, null=True)
    author = models.ManyToManyField(Author, related_name="publication_author", verbose_name="Об авторе", blank=True)
    book = models.ManyToManyField(Book, related_name="publication_book", verbose_name="О книге", blank=True)
    series = models.ManyToManyField(Series, related_name="publication_series", blank=True)
    user = models.ForeignKey(User, verbose_name="Автор публикации", null=True, on_delete=models.DO_NOTHING)
    date_create = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    date_update = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    show_counter = models.PositiveIntegerField('Количество просмотров', default=0, null=True)

    def __str__(self):
        return "{0}".format(self.title)

    def get_type(self):
        return 'publication'

    def get_absolute_url(self):
        return "/publication/%i/" % self.id

    class Meta:
        ordering = ['-id']
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'
