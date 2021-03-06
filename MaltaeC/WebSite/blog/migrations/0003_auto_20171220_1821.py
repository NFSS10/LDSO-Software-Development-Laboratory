# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-20 18:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20171220_1518'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image1',
            field=models.ImageField(blank=True, upload_to='blog/'),
        ),
        migrations.AlterField(
            model_name='post',
            name='image2',
            field=models.ImageField(blank=True, upload_to='blog/'),
        ),
        migrations.AlterField(
            model_name='post',
            name='image3',
            field=models.ImageField(blank=True, upload_to='blog/'),
        ),
        migrations.AlterField(
            model_name='post',
            name='image4',
            field=models.ImageField(blank=True, upload_to='blog/'),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(default='', max_length=100),
        ),
    ]
