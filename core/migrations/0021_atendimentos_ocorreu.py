# Generated by Django 4.2.6 on 2024-01-30 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_alter_atendimentos_motivofalta'),
    ]

    operations = [
        migrations.AddField(
            model_name='atendimentos',
            name='ocorreu',
            field=models.BooleanField(default=False),
        ),
    ]
