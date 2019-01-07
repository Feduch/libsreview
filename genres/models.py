from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.urls import reverse


class Genre(models.Model):
    """Модель жанры"""
    title = models.CharField(verbose_name='Название', max_length=255)
    slug = models.SlugField(max_length=255, default='')
    description = models.TextField(verbose_name='Описание жанра')
    parent = models.ForeignKey('self', related_name="children", on_delete=models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('genre-detail', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['title']
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class ParentGenre(models.Model):
    name = models.CharField('Раздел', max_length=300)

    def __str__(self):
        return self.name


class GenreNew(models.Model):
    """Модель жанры"""
    name = models.CharField('Название', max_length=300)
    name_eng = models.CharField('Название на английском', max_length=300, blank=True, null=True)
    slug = models.SlugField(max_length=255, default='')
    description = models.TextField('Описание жанра', blank=True, null=True)
    parent = models.ForeignKey(ParentGenre, on_delete=models.DO_NOTHING, blank=True, null=True)
    flibusta_id = models.PositiveIntegerField('Идентификатор на флибусте', blank=True, null=True)
    litres_id = models.PositiveIntegerField('Идентификатор на литресе (не факт:)', blank=True, null=True)
    genre_litres = ArrayField(models.PositiveIntegerField(), blank=True)
    date_update = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('genre-detail', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['name']
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
