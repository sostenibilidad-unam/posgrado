# Generated by Django 3.0.6 on 2021-06-03 01:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posgradmin', '0076_auto_20210602_2006'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='membresiacomite',
            options={'ordering': ['year', 'semestre'], 'verbose_name_plural': 'Membresías de Comités Tutorales'},
        ),
    ]
