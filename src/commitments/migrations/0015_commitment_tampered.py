# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-28 04:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commitments', '0014_auto_20170227_2324'),
    ]

    operations = [
        migrations.AddField(
            model_name='commitment',
            name='tampered',
            field=models.BooleanField(default=False),
        ),
    ]