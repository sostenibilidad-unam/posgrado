# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-06 21:49
from __future__ import unicode_literals

from django.db import migrations, models
import posgradmin.models


class Migration(migrations.Migration):

    dependencies = [
        ('posgradmin', '0007_academico_anexo_estimulo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='academico',
            name='anexo_estimulo',
            field=models.FileField(blank=True, null=True, verbose_name=b'Documento probatorio de Est\xc3\xadmulo UNAM'),
        ),
    ]
