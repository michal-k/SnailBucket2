# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-05-01 17:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0002_auto_20160501_1725'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='result',
            field=models.CharField(blank=True, choices=[('1-0', '1-0'), ('+:-', '+:-'), ('0-1', '0-1'), ('-:+', '-:+'), ('-:-', '-:-'), ('1/2-1/2', '1/2-1/2')], help_text='Game status/result.', max_length=16, null=True),
        ),
    ]
