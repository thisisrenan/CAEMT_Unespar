from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField




class User(AbstractUser):
    class Role(models.TextChoices):
        SUPERVISOR = "SUPERVISOR", 'supervisor'
        ORIENTADOR = "ORIENTADOR", 'orientador'
        ESTAGIARIO = "ESTAGIARIO", 'estagiario'

    email = models.EmailField(unique=True, verbose_name='Email')
    username = models.CharField(unique=True, verbose_name='Username', max_length=10)
    biografia = models.CharField(verbose_name='Bio', max_length=50, default='')
    outrasinformacoes = models.CharField(verbose_name='Bio', max_length=500, default='')
    image = models.ImageField(upload_to='pics', default='padrao.png')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    base_role = Role.SUPERVISOR
    data_final = models.DateField(verbose_name='Data Final', null=True, blank=True)
    role = models.CharField(max_length=50, choices=Role.choices)

    class Meta:
        verbose_name_plural = "Supervisor"
    def save(self, *arg, **kwargs):
        if not self.pk:
            self.role = self.base_role
            return super().save(*arg, **kwargs)


class Orientador(User):
    base_role = User.Role.ORIENTADOR
    data_de_nascimento = models.DateField(verbose_name='Nascimento', blank=True)
    telefone = PhoneNumberField(verbose_name='Telefone', blank=True)

    class Meta:
        verbose_name_plural = "Orientador"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.set_password(self.password)
            self.role = self.base_role
        super().save(*args, **kwargs)
    def welcome(self):
        return "Only Orientador"





class Estagiario(User):
    base_role = User.Role.ESTAGIARIO
    ano_letivo = models.IntegerField(verbose_name='Ano', blank=True, default=3)
    data_de_nascimento = models.DateField(verbose_name='Nascimento', blank=True)
    telefone = PhoneNumberField(verbose_name='Telefone', blank=True)
    orientador_responsavel = models.ForeignKey(Orientador, on_delete=models.SET_NULL, null=True, blank=True, related_name='estagiarios', verbose_name='Orientador')

    class Meta:
        verbose_name_plural = "Estagiario"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.set_password(self.password)
            self.role = self.base_role
        super().save(*args, **kwargs)
    def welcome(self):
        return "Only Estagiario"







class Participante(models.Model):
    nome = models.CharField(max_length=100)
    sobrenome = models.CharField(max_length=100)
    data_de_nascimento = models.DateField(verbose_name='Nascimento', blank=True)
    telefone = PhoneNumberField(verbose_name='Telefone', blank=True)
    motivo_busca_atendimento = models.TextField(verbose_name='Motivo da Busca por Atendimento', blank=True)
    estagiarios = models.ManyToManyField(Estagiario, related_name='participante_profiles', blank=True)


class Endereco(models.Model):
    cep = models.CharField(verbose_name='CEP', max_length=8)
    numero = models.CharField(verbose_name='Número', max_length=10)
    complemento = models.CharField(verbose_name='Complemento', max_length=255, blank=True)
    cidade = models.CharField(verbose_name='Cidade', max_length=100, blank=True)
    estado = models.CharField(verbose_name='estado', max_length=100, blank=True)
    bairro = models.CharField(verbose_name='Bairro', max_length=100, blank=True)
    av_r = models.CharField(verbose_name="AV", max_length=300,  blank=True)
    participante = models.OneToOneField(Participante, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Endereço')
