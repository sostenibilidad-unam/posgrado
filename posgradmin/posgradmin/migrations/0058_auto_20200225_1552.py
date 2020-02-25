# Generated by Django 3.0.3 on 2020-02-25 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posgradmin', '0057_auto_20200215_1737'),
    ]

    operations = [
        migrations.AlterField(
            model_name='academico',
            name='nivel_SNI',
            field=models.CharField(blank=True, choices=[('sin SNI', 'sin SNI'), ('I', 'I'), ('II', 'II'), ('III', 'III'), ('C', 'C'), ('E', 'E')], default='sin SNI', max_length=15, null=True, verbose_name='Nivel SNI'),
        ),
    ]
