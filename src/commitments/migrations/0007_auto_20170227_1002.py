# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-27 10:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commitments', '0006_commitmentreadability_readable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commitmentreadability',
            name='readable',
            field=models.CharField(max_length=1),
        ),
    ]