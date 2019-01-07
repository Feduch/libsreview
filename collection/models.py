from django.db import models
from django.contrib.auth.models import User
from books.models import Book


def collection_image_path(instance, filename):
    return 'collections/{0}/{1}'.format(instance.user.id, filename)


class Collection(models.Model):
    title = models.CharField(verbose_name='Название коллекции', max_length=255)
    text = models.TextField(verbose_name='Описание')
    image = models.ImageField(verbose_name='Обложка', upload_to=collection_image_path, blank=True, null=True)
    rating = models.DecimalField('Рейтинг', default=0, max_digits=3, decimal_places=2)
    book = models.ManyToManyField(Book, related_name="collections_book", verbose_name="книги")
    user = models.ForeignKey(User, verbose_name="Автор коллекции", null=True, on_delete=models.DO_NOTHING)
    date_create = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    date_update = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    show_counter = models.PositiveIntegerField('Количество просмотров', default=0)
    is_award = models.BooleanField('Коллекция является премией?', default=False)

    def get_type(self):
        return 'collection'

    def __str__(self):
        return "{0}".format(self.title)

    def get_absolute_url(self):
        return "/collections/%i/" % self.id

    class Meta:
        ordering = ['-date_create']
        verbose_name = 'Коллекцию'
        verbose_name_plural = 'Коллекции'
