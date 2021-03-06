# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-21 16:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posgradmin', '0012_auto_20180921_1118'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='estudiante',
            name='fecha_titulacion',
        ),
        migrations.RemoveField(
            model_name='estudiante',
            name='folio_titulacion',
        ),
        migrations.AddField(
            model_name='estudiante',
            name='anno_graduacion',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='a\xf1o de graduaci\xf3n'),
        ),
        migrations.AddField(
            model_name='estudiante',
            name='fecha_graduacion',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha de graduaci\xf3n'),
        ),
        migrations.AddField(
            model_name='estudiante',
            name='folio_graduacion',
            field=models.CharField(blank=True, max_length=200, verbose_name='Folio de acta de examen de grado'),
        ),
        migrations.AlterField(
            model_name='estudiante',
            name='institucion',
            field=models.ForeignKey(blank=True, help_text='Instituci\xf3n de Inscripci\xf3n', null=True, on_delete=django.db.models.deletion.CASCADE, to='posgradmin.Institucion'),
        ),
        migrations.AlterField(
            model_name='estudiante',
            name='medalla_alfonso_caso',
            field=models.BooleanField(default=False, verbose_name='Medalla Alfonso Caso'),
        ),
        migrations.AlterField(
            model_name='estudiante',
            name='semestre_graduacion',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='semestre de graduaci\xf3n'),
        ),
    ]
