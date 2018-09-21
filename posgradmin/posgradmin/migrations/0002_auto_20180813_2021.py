# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-08-14 01:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import posgradmin.models


class Migration(migrations.Migration):

    dependencies = [
        ('posgradmin', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='anexoacademico',
            name='academico',
        ),
        migrations.RemoveField(
            model_name='anexoacademico',
            name='autor',
        ),
        migrations.AlterModelOptions(
            name='adscripcion',
            options={'verbose_name_plural': 'Adscripciones'},
        ),
        migrations.AddField(
            model_name='academico',
            name='anexo_CV',
            field=models.FileField(blank=True, null=True, upload_to=posgradmin.models.anexo_academico_CV_path, verbose_name=b'CV en extenso'),
        ),
        migrations.AddField(
            model_name='academico',
            name='anexo_SNI',
            field=models.FileField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='academico',
            name='anexo_solicitud',
            field=models.FileField(blank=True, null=True, upload_to=posgradmin.models.anexo_academico_solicitud_path, verbose_name=b'Carta de solicitud de acreditaci\xc3\xb3n como tutor'),
        ),
        migrations.AlterField(
            model_name='estudiante',
            name='institucion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='posgradmin.Institucion'),
        ),
        migrations.DeleteModel(
            name='AnexoAcademico',
        ),
    ]