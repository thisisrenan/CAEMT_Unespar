# Generated by Django 4.2.6 on 2023-12-20 15:08

import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_alter_user_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Endereco',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cep', models.IntegerField(max_length=8, verbose_name='CEP')),
                ('numero', models.CharField(max_length=10, verbose_name='Número')),
                ('complemento', models.CharField(blank=True, max_length=255, verbose_name='Complemento')),
                ('cidade', models.CharField(blank=True, max_length=100, verbose_name='Cidade')),
                ('estado', models.CharField(blank=True, max_length=100, verbose_name='estado')),
                ('bairro', models.CharField(blank=True, max_length=100, verbose_name='Bairro')),
            ],
        ),
        migrations.CreateModel(
            name='Participante',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('core.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='outrasinformacoes',
            field=models.CharField(default='', max_length=500, verbose_name='Bio'),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('SUPERVISOR', 'supervisor'), ('ORIENTADOR', 'orientador'), ('ESTAGIARIO', 'estagiario'), ('PARTICIPANTE', 'participante')], max_length=50),
        ),
        migrations.CreateModel(
            name='ParticipanteProfile',
            fields=[
                ('participante_id', models.IntegerField(primary_key=True, serialize=False, verbose_name='ID')),
                ('data_de_nascimento', models.DateField(blank=True, verbose_name='Nascimento')),
                ('telefone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None, verbose_name='Telefone')),
                ('motivo_busca_atendimento', models.TextField(blank=True, verbose_name='Motivo da Busca por Atendimento')),
                ('endereco', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.endereco', verbose_name='Endereço')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.participante')),
            ],
        ),
    ]
