# Generated by Django 4.2.6 on 2024-01-12 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_user_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='participante',
            name='username',
            field=models.CharField(default=0, max_length=10, unique=True, verbose_name='Username'),
            preserve_default=False,
        ),
    ]