# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-10-18 21:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posgradmin', '0016_auto_20181003_1216'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='academico',
            name='DGEE',
        ),
        migrations.AddField(
            model_name='academico',
            name='comite_doctorado_otros',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name=b'Cantidad total de participaciones como miembro de comit\xc3\xa9\n        tutor (no tutor principal) de estudiantes graduados de nivel\n        doctorado en otros programas.'),
        ),
        migrations.AddField(
            model_name='academico',
            name='comite_maestria_otros',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name=b'Cantidad total de participaciones como miembro de comit\xc3\xa9\n        tutor (no tutor principal) de estudiantes graduados de nivel\n        maestr\xc3\xada en otros programas.'),
        ),
        migrations.AddField(
            model_name='academico',
            name='otras_actividades',
            field=models.TextField(blank=True, null=True, verbose_name=b'Si no cuenta con estudiantes graduados, indique si cuenta con\n        otras actividades acad\xc3\xa9micas como estancias de investigaci\xc3\xb3n,\n        seminarios de titulaci\xc3\xb3n, etc.'),
        ),
        migrations.AddField(
            model_name='academico',
            name='otras_publicaciones',
            field=models.TextField(blank=True, null=True, verbose_name=b'Si su productividad acad\xc3\xa9mica no se ve reflejada en las\n        publicaciones anteriores, indique si cuenta con otros\n        productos como por ejemplo informes t\xc3\xa9cnicos, memorias\n        t\xc3\xa9cnicas, desarrollo de proyectos hasta nivel ejecutivo,\n        planes y programas de desarrollo urbano, manuales, etc.'),
        ),
        migrations.AlterField(
            model_name='academico',
            name='participacion_comite_doctorado',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name=b'Cantidad de participaciones como miembro de comit\xc3\xa9 tutor (no tutor\n        principal) en el Posgrado en Ciencias de la Sostenibilidad a\n        nivel doctorado'),
        ),
        migrations.AlterField(
            model_name='academico',
            name='participacion_comite_maestria',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name=b'Cantidad de participaciones como miembro de comit\xc3\xa9 tutor (no tutor\n         principal) en el Posgrado en Ciencias de la Sostenibilidad a\n         nivel maestr\xc3\xada'),
        ),
        migrations.AlterField(
            model_name='academico',
            name='participacion_tutor_doctorado',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name=b'Cantidad de participaciones como tutor principal en el Posgrado en\n           Ciencias de la Sostenibilidad a nivel doctorado'),
        ),
        migrations.AlterField(
            model_name='academico',
            name='participacion_tutor_maestria',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name=b'Cantidad de participaciones como tutor principal en el\n        Posgrado en Ciencias de la Sostenibilidad a nivel maestr\xc3\xada'),
        ),
        migrations.AlterField(
            model_name='academico',
            name='tesis_doctorado',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name=b'Cantidad total de participaciones como tutor principal de\n        estudiantes graduados de nivel Doctorado'),
        ),
        migrations.AlterField(
            model_name='academico',
            name='tesis_doctorado_5',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name=b'Cantidad de participaciones como tutor principal de\n        estudiantes graduados de nivel Doctorado en los \xc3\xbaltimos 5 a\xc3\xb1os'),
        ),
        migrations.AlterField(
            model_name='academico',
            name='tesis_licenciatura',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name=b'Cantidad total de participaciones como tutor principal de\n        estudiantes graduados de nivel Licenciatura'),
        ),
        migrations.AlterField(
            model_name='academico',
            name='tesis_licenciatura_5',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name=b'Cantidad de participaciones como tutor principal de\n        estudiantes " graduados a nivel Licenciatura en los \xc3\xbaltimos 5\n        a\xc3\xb1os'),
        ),
        migrations.AlterField(
            model_name='academico',
            name='tesis_maestria',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name=b'Cantidad total participaciones como tutor principal de estudiantes\n        graduados de nivel Maestr\xc3\xada'),
        ),
        migrations.AlterField(
            model_name='academico',
            name='tesis_maestria_5',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name=b'Cantidad de participaciones como tutor principal de estudiantes\n           graduados de nivel Maestr\xc3\xada en los \xc3\xbaltimos 5 a\xc3\xb1os'),
        ),
        migrations.AlterField(
            model_name='academico',
            name='tutor_otros_programas',
            field=models.TextField(blank=True, verbose_name=b'Nombres de los otros programas en los que participa como miembro de\n        comit\xc3\xa9 tutor (no tutor principal).'),
        ),
        migrations.AlterField(
            model_name='academico',
            name='tutor_principal_otros_programas',
            field=models.TextField(blank=True, verbose_name=b'Nombres de los otros programas en los que participa como tutor\n           principal'),
        ),
    ]
