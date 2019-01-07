from django.db import models


def series_image_path(instance, filename):
    return 'series/{0}/{1}'.format(instance.id, filename)


class Series(models.Model):
    title = models.CharField(verbose_name='Название серии', max_length=255)
    description = models.TextField(verbose_name='Описание серии')
    image = models.ImageField(verbose_name='Обложка серии', upload_to=series_image_path, blank=True, null=True)
    rating = models.DecimalField('Рейтинг', default=0, max_digits=3, decimal_places=2)
    show_counter = models.PositiveIntegerField('Количество просмотров', default=0)
    date_create = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    date_update = models.DateTimeField(auto_now_add=True, null=True, blank=True, help_text="Дата обновления")
    status = models.NullBooleanField(
        'Да - проверена и опубликована, Нет - проверена и отключена, Неизвестно - на проверке')
    litres_id = models.CharField(verbose_name='ID на литресе', max_length=36, blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return "/book/series/%i.html" % self.id

    class Meta:
        ordering = ['-id']
        verbose_name = 'Серия'
        verbose_name_plural = 'Серии'
