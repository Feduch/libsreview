from django.db import models
from django.urls import reverse


class Award(models.Model):
    name = models.CharField('Название премии', max_length=255, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('award-detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['name']
        verbose_name = 'Премия'
        verbose_name_plural = 'Премии'
