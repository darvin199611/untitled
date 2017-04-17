from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import render
from django.utils import timezone


class Market(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=20, default="market")
    description = models.TextField()
    picture = models.ImageField(upload_to='market_images', blank=True)
    created = models.DateTimeField('Создан', default=timezone.now, auto_now=False)
    updated = models.DateTimeField('Изменен', auto_now_add=False, auto_now=True)

    def list(request):
        usr = request.user
        markets = Market.objects.filter(user=usr).order_by('created')
        return markets

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Мвгазин"
        verbose_name_plural = "Магазины"


class Stuff(models.Model):
    market = models.ForeignKey(Market, verbose_name='Магазин')
    name = models.CharField('Название', max_length=200)
    description = models.TextField('Описание', blank=True)
    picture = models.ImageField('Каритнка', upload_to='stuff_images', blank=True)
    price = models.DecimalField('Цена', max_digits=8, decimal_places=2, default=0)
    amount = models.PositiveIntegerField('Количество на складе', default=0)
    created = models.DateTimeField('Создан', default=timezone.now, auto_now=False)
    updated = models.DateTimeField('Изменен', auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class UserProfile(models.Model):
    # Эта строка обязательна. Она связывает UserProfile с экземпляром модели User.
    user = models.OneToOneField(User)
    # Дополнительные атрибуты, которые мы хотим добавить.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    created = models.DateTimeField('Создан', default=timezone.now, auto_now=False)
    updated = models.DateTimeField('Изменен', auto_now_add=False, auto_now=True)
    # Переопределяем метод __unicode__(), чтобы вернуть что-либо значимое! Используйте __str__() в Python 3.*

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"


class Sale(models.Model):
    stuff = models.ForeignKey(Stuff)
    created = models.DateTimeField('Создан', default=timezone.now, auto_now=False)

    class Meta:
        ordering = ['created']
        verbose_name = "Продажа"
        verbose_name_plural = "Продажи"

    def __str__(self):
        return self.stuff.name


