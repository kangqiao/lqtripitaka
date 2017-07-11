# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-11 05:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20170710_2219'),
    ]

    operations = [
        migrations.AddField(
            model_name='roll',
            name='end_volume',
            field=models.UUIDField(blank=True, null=True, verbose_name='终止册'),
        ),
        migrations.AddField(
            model_name='roll',
            name='start_volume',
            field=models.UUIDField(blank=True, null=True, verbose_name='起始册'),
        ),
        migrations.AlterField(
            model_name='sutra',
            name='lqsutra',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lqsutra_list', to='core.LQSutra', verbose_name='龙泉收录'),
        ),
    ]
