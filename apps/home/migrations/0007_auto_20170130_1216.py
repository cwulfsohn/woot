# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-30 18:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_auto_20170130_1214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='expire_date',
            field=models.DateTimeField(default=None),
        ),
    ]