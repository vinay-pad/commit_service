# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-27 01:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('commitments', '0002_commitment_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='commitment',
            name='created_ts',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
