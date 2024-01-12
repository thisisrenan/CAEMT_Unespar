# Generated by Django 4.2.6 on 2024-01-12 12:52

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_remove_participante_data_de_nascimento'),
    ]

    operations = [
        migrations.AddField(
            model_name='participante',
            name='date_final',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Date Final'),
        ),
        migrations.AddField(
            model_name='participante',
            name='date_joined',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Date Joined'),
            preserve_default=False,
        ),
    ]
