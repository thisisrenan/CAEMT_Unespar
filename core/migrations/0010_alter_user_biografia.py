# Generated by Django 4.2.6 on 2023-12-19 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_user_biografia_user_image_alter_user_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='biografia',
            field=models.CharField(default='', max_length=50, verbose_name='Bio'),
        ),
    ]
