# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-13 14:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0004_market_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stuff',
            name='published_date',
        ),
    ]