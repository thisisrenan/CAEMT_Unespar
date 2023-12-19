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
    username = models.EmailField(unique=True, verbose_name='Username')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    base_role = Role.SUPERVISOR
    data_final = models.DateField(verbose_name='Data Final', null=True, blank=True)
    role = models.CharField(max_length=50, choices=Role.choices)

    def save(self, *arg, **kwargs):
        if not self.pk:
            self.role = self.base_role
            return super().save(*arg, **kwargs)


class Orientador(User):
    base_role = User.Role.ORIENTADOR

    class Meta:
        proxy = True

    def welcome(self):
        return "Only Orientador"

    @classmethod
    def create_users(cls, username, password, email, nascimento, telefone):
        Orientador = cls.objects.create_user(username=username, password=password, email=email)
        Profile = OrientadorProfile.objects.create(user=Orientador, data_de_nascimento=nascimento, telefone=telefone)
        return Orientador
        print("Sucesso demais Orientador")


class OrientadorProfile(models.Model):
    user = models.OneToOneField(Orientador, on_delete=models.CASCADE)
    orientador_id = models.IntegerField(verbose_name='ID', primary_key=True)
    data_de_nascimento = models.DateField(verbose_name='Nascimento', blank=True)
    telefone = PhoneNumberField(verbose_name='Telefone', blank=True)

class Estagiario(User):
    base_role = User.Role.ESTAGIARIO

    class Meta:
        proxy = True

    def welcome(self):
        return "Only Estagiario"

    @classmethod
    def create_users(cls, username, password, email, nascimento, telefone, orientador, ano_letivo):
        estagiario = cls.objects.create_user(username=username, password=password, email=email)
        EstagiarioProfile.objects.create(user=estagiario, data_de_nascimento=nascimento, telefone=telefone, orientador=orientador, ano_letivo=ano_letivo)
        print("Sucesso demais")


class EstagiarioProfile(models.Model):
    user = models.OneToOneField(Estagiario, on_delete=models.CASCADE)
    estagiario_id = models.IntegerField(verbose_name='ID', primary_key=True)
    ano_letivo = models.IntegerField(verbose_name='Ano', blank=True, default=3)
    data_de_nascimento = models.DateField(verbose_name='Nascimento', blank=True)
    telefone = PhoneNumberField(verbose_name='Telefone', blank=True)
    orientador = models.ForeignKey(Orientador, on_delete=models.SET_NULL, null=True, blank=True, related_name='estagiarios', verbose_name='Orientador')
