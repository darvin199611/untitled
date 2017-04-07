from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import render
from django.utils import timezone


class Market(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=20, default="market")
    description = models.TextField()
    created_date = models.DateTimeField(
        default=timezone.now)
    picture = models.ImageField(upload_to='market_images', blank=True)

    def spisok(request):
        usr = request.user
        markets = Market.objects.filter(user=usr).order_by('created_date')
        return markets

    def __str__(self):
        return self.name


class Stuff(models.Model):
    market = models.ForeignKey(Market, verbose_name='Магазин')
    name = models.CharField('Название', max_length=200)
    description = models.TextField('Описание', blank=True)
    created_date = models.DateTimeField('Дата создания',
                                        default=timezone.now)
    picture = models.ImageField('Каритнка', upload_to='stuff_images', blank=True)
    price = models.DecimalField('Цена', max_digits=8, decimal_places=2, default=0)
    amount = models.PositiveIntegerField('Количество на складе', default=0)

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


class Sale(models.Model):
    stuff = models.ForeignKey(Stuff)
    datetime = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['datetime']

    def __str__(self):
        return self.stuff.name
