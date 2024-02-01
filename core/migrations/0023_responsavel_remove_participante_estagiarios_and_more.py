# Generated by Django 4.2.6 on 2024-01-31 13:39

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_participante_qtd_atendimentos'),
    ]

    operations = [
        migrations.CreateModel(
            name='Responsavel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('sobrenome', models.CharField(max_length=100)),
                ('telefone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, verbose_name='Telefone')),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.RemoveField(
            model_name='participante',
            name='estagiarios',
        ),
        migrations.AddField(
            model_name='participante',
            name='data_de_nascimento',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='participante',
            name='escola',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='participante',
            name='serie',
            field=models.IntegerField(blank=True, null=True, verbose_name='serie'),
        ),
        migrations.AlterField(
            model_name='participante',
            name='telefone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, verbose_name='Telefone'),
        ),
        migrations.AddField(
            model_name='participante',
            name='responsavel',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.responsavel'),
        ),
    ]
