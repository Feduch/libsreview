from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from sorl.thumbnail import get_thumbnail


# Create your models here.
def user_directory_path(instance, filename):
    return 'profile/{0}/{1}'.format(instance.user.id, filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField('Аватар', upload_to=user_directory_path, blank=True, null=True)
    rating = models.DecimalField('Рейтинг', default=0, max_digits=3, decimal_places=2)
    description = models.TextField('Описание',blank=True, null=True)

    def __str__(self):
        return self.user.username

    def get_avatar_small(self):
        if self.avatar:
            im = get_thumbnail(self.avatar, '48x48', crop='center', quality=80)
            return im.url
        else:
            return 'data:image/svg+xml;charset=UTF-8,%3Csvg%20width%3D%2275%22%20height%3D%2275%22%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2075%2075%22%20preserveAspectRatio%3D%22none%22%3E%3Cdefs%3E%3Cstyle%20type%3D%22text%2Fcss%22%3E%23holder_16571ccf1dd%20text%20%7B%20fill%3Argba(255%2C255%2C255%2C.75)%3Bfont-weight%3Anormal%3Bfont-family%3AHelvetica%2C%20monospace%3Bfont-size%3A10pt%20%7D%20%3C%2Fstyle%3E%3C%2Fdefs%3E%3Cg%20id%3D%22holder_16571ccf1dd%22%3E%3Crect%20width%3D%2275%22%20height%3D%2275%22%20fill%3D%22%23777%22%3E%3C%2Frect%3E%3Cg%3E%3Ctext%20x%3D%2218.5546875%22%20y%3D%2242%22%3E75x75%3C%2Ftext%3E%3C%2Fg%3E%3C%2Fg%3E%3C%2Fsvg%3E'

    class Meta:
        ordering = ['-id']
        verbose_name = 'Профайл'
        verbose_name_plural = 'Профайлы'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)