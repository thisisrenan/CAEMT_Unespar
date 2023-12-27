from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField

class Endereco(models.Model):
    cep = models.CharField(verbose_name='CEP', max_length=8)
    numero = models.CharField(verbose_name='Número', max_length=10)
    complemento = models.CharField(verbose_name='Complemento', max_length=255, blank=True)
    cidade = models.CharField(verbose_name='Cidade', max_length=100, blank=True)
    estado = models.CharField(verbose_name='estado', max_length=100, blank=True)
    bairro = models.CharField(verbose_name='Bairro', max_length=100, blank=True)
    av_r = models.CharField(verbose_name="AV", max_length=300,  blank=True)


class User(AbstractUser):
    class Role(models.TextChoices):
        SUPERVISOR = "SUPERVISOR", 'supervisor'
        ORIENTADOR = "ORIENTADOR", 'orientador'
        ESTAGIARIO = "ESTAGIARIO", 'estagiario'
        PARTICIPANTE = "PARTICIPANTE", 'participante'

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


class Participante(User):
    base_role = User.Role.PARTICIPANTE

    class Meta:
        proxy = True

    def welcome(self):
        return "Only Orientador"

    @classmethod
    def create_users(cls, username, email, nascimento, telefone, motivobusca, cep, numero, complemento, cidade, estado,
                     bairro, av, estagiarios=None):
        participante = cls.objects.create_user(username=username, password="123", email=email)
        endereco = Endereco.objects.create(cep=cep, numero=numero, complemento=complemento, cidade=cidade,
                                           estado=estado, bairro=bairro, av_r=av)
        profile = ParticipanteProfile.objects.create(user=participante, data_de_nascimento=nascimento,
                                                     telefone=telefone, motivo_busca_atendimento=motivobusca,
                                                     endereco=endereco)

        if estagiarios:
            profile.estagiarios.set(estagiarios)

        print("Sucesso demais Participante")
        return participante


class ParticipanteProfile(models.Model):
    user = models.OneToOneField(Participante, on_delete=models.CASCADE)
    participante_id = models.AutoField(verbose_name='ID', primary_key=True, )
    data_de_nascimento = models.DateField(verbose_name='Nascimento', blank=True)
    telefone = PhoneNumberField(verbose_name='Telefone', blank=True)
    motivo_busca_atendimento = models.TextField(verbose_name='Motivo da Busca por Atendimento', blank=True)
    endereco = models.OneToOneField(Endereco, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Endereço')
    estagiarios = models.ManyToManyField(Estagiario, related_name='participante_profiles', blank=True)