# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-27 19:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('commitments', '0008_auto_20170227_1918'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commitmentreadability',
            name='commitment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='readability', to='commitments.Commitment', unique=True),
        ),
    ]