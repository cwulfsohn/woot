# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-31 20:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='deal_date',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]
