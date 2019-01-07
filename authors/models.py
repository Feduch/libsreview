from django.db import models
from django.urls import reverse
from awards.models import Award


class Nationality(models.Model):
    country = models.CharField('Страна', max_length=100)
    nationality = models.CharField('Национальность', max_length=100)
    slug = models.SlugField(max_length=100, default='')

    def __str__(self):
        return "{} - {}".format(self.nationality, self.country)

    def get_absolute_url(self):
        return reverse('country-detail', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['country']
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'


def author_image_path(instance, filename):
    return 'authors/{0}/{1}'.format(instance.id, filename)


class Author(models.Model):
    name = models.CharField(verbose_name='Автор', max_length=100)
    litres_name = models.CharField(verbose_name='Имя на литресе', max_length=100, blank=True, null=True)
    description = models.TextField(verbose_name='Описание автора', blank=True, null=True)
    photo = models.ImageField(verbose_name='Фото автора', upload_to=author_image_path, blank=True, null=True)
    birthday = models.CharField(verbose_name='Дата рождения', max_length=50, blank=True, null=True)
    death = models.CharField(verbose_name='Дата смерти', max_length=50, blank=True, null=True)
    name_original = models.CharField(verbose_name='Оригинальное имя', max_length=100, blank=True, null=True)
    rating = models.DecimalField('Рейтинг', default=0, max_digits=2, decimal_places=1)
    rating = models.DecimalField('Рейтинг', default=0, max_digits=3, decimal_places=2)
    date_create = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    date_update = models.DateTimeField(auto_now=True, null=True, blank=True, help_text="Дата обновления")
    show_counter = models.PositiveIntegerField('Количество просмотров', default=0, null=True)
    book_count = models.PositiveIntegerField('Количество книг', default=0, null=True)
    status = models.NullBooleanField(
        'Да - проверен и опубликован, Нет - проверен и отключен, Неизвестно - на проверке')
    litres_id = models.CharField(verbose_name='ID на литресе', max_length=36, blank=True, null=True)
    nationality = models.ForeignKey(Nationality, blank=True, null=True, on_delete=models.DO_NOTHING)
    is_active = models.BooleanField('Активен', default=True)
    award = models.ManyToManyField(Award, related_name="author_award", blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return "/a/%i/" % self.id

    def get_photo(self):
        photo = '/static/images/default_avatar.png'
        if self.photo:
            if 'http' in self.photo.url:
                photo = self.photo.url.replace('/media/', '').replace('%3A', ':')
            else:
                photo = self.photo.url
        return photo

    class Meta:
        ordering = ['-rating', '-show_counter']
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'