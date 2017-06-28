# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-28 14:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20170623_0016'),
    ]

    operations = [
        migrations.AddField(
            model_name='series',
            name='book_reservation',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='典藏号'),
        ),
        migrations.AddField(
            model_name='series',
            name='library_site',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='馆藏地'),
        ),
        migrations.AddField(
            model_name='sutra',
            name='end_volume',
            field=models.UUIDField(blank=True, null=True, verbose_name='终止册'),
        ),
        migrations.AddField(
            model_name='sutra',
            name='start_volume',
            field=models.UUIDField(blank=True, null=True, verbose_name='起始册'),
        ),
        migrations.AlterField(
            model_name='series',
            name='dynasty',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='刊刻时间'),
        ),
        migrations.AlterField(
            model_name='series',
            name='historic_site',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='刊刻地点'),
        ),
    ]
