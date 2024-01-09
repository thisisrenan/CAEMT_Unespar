# Generated by Django 4.2.6 on 2024-01-09 11:19

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Estagiario',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('ano_letivo', models.IntegerField(blank=True, default=3, verbose_name='Ano')),
                ('data_de_nascimento', models.DateField(blank=True, verbose_name='Nascimento')),
                ('telefone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None, verbose_name='Telefone')),
            ],
            options={
                'verbose_name_plural': 'Estagiario',
            },
            bases=('core.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Orientador',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('data_de_nascimento', models.DateField(blank=True, verbose_name='Nascimento')),
                ('telefone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None, verbose_name='Telefone')),
            ],
            options={
                'verbose_name_plural': 'Orientador',
            },
            bases=('core.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name_plural': 'Supervisor'},
        ),
        migrations.AddField(
            model_name='user',
            name='biografia',
            field=models.CharField(default='', max_length=50, verbose_name='Bio'),
        ),
        migrations.AddField(
            model_name='user',
            name='data_final',
            field=models.DateField(blank=True, null=True, verbose_name='Data Final'),
        ),
        migrations.AddField(
            model_name='user',
            name='image',
            field=models.ImageField(default='padrao.png', upload_to='pics'),
        ),
        migrations.AddField(
            model_name='user',
            name='outrasinformacoes',
            field=models.CharField(default='', max_length=500, verbose_name='Bio'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=10, unique=True, verbose_name='Username'),
        ),
        migrations.CreateModel(
            name='Participante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('sobrenome', models.CharField(max_length=100)),
                ('data_de_nascimento', models.DateField(blank=True, verbose_name='Nascimento')),
                ('telefone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None, verbose_name='Telefone')),
                ('motivo_busca_atendimento', models.TextField(blank=True, verbose_name='Motivo da Busca por Atendimento')),
                ('estagiarios', models.ManyToManyField(blank=True, related_name='participante_profiles', to='core.estagiario')),
            ],
        ),
        migrations.AddField(
            model_name='estagiario',
            name='orientador_responsavel',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='estagiarios', to='core.orientador', verbose_name='Orientador'),
        ),
        migrations.CreateModel(
            name='Endereco',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cep', models.CharField(max_length=8, verbose_name='CEP')),
                ('numero', models.CharField(max_length=10, verbose_name='Número')),
                ('complemento', models.CharField(blank=True, max_length=255, verbose_name='Complemento')),
                ('cidade', models.CharField(blank=True, max_length=100, verbose_name='Cidade')),
                ('estado', models.CharField(blank=True, max_length=100, verbose_name='estado')),
                ('bairro', models.CharField(blank=True, max_length=100, verbose_name='Bairro')),
                ('av_r', models.CharField(blank=True, max_length=300, verbose_name='AV')),
                ('participante', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.participante', verbose_name='Endereço')),
            ],
        ),
    ]