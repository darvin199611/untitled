from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Market(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=20, default="market")
    description = models.TextField()
    created_date = models.DateTimeField(
        default=timezone.now)
    picture = models.ImageField(upload_to='market_images', blank=True)

    def __str__(self):
        return self.name


class Stuff(models.Model):
    market = models.ForeignKey(Market)
    name = models.CharField(max_length=200, )
    description = models.TextField()
    created_date = models.DateTimeField(
        default=timezone.now)
    picture = models.ImageField(upload_to='stuff_images', blank=True)
    price = models.DecimalField('Цена', max_digits=8, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    # Эта строка обязательна. Она связывает UserProfile с экземпляром модели User.
    user = models.OneToOneField(User)

    # Дополнительные атрибуты, которые мы хотим добавить.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    # Переопределяем метод __unicode__(), чтобы вернуть что-либо значимое! Используйте __str__() в Python 3.*
    def __str__(self):
        return self.user.username