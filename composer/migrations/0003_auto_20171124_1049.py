# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-24 10:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('composer', '0002_auto_20170126_0518'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='column',
            options={'ordering': ['position']},
        ),
        migrations.AlterModelOptions(
            name='row',
            options={'ordering': ['position']},
        ),
        migrations.AlterModelOptions(
            name='tile',
            options={'ordering': ['position']},
        ),
    ]