# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-02 14:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
        ('home', '0002_remove_purchase_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='user_purchase', to='login.User'),
            preserve_default=False,
        ),
    ]