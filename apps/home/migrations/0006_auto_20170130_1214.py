# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-30 18:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_auto_20170130_1131'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='list_price',
            field=models.FloatField(default=None),
        ),
        migrations.AddField(
            model_name='product',
            name='name',
            field=models.CharField(default=None, max_length=255),
        ),
    ]