# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-09 05:09
from __future__ import unicode_literals

import blog.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=200, validators=[blog.models.min_length_3_validator]),
        ),
    ]
