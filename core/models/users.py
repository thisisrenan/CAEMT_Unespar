from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField

def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = f"{instance.username}"
    full_path = f'pics/{new_filename}.{ext}'
    return full_path


class User(AbstractUser):
    class Role(models.TextChoices):
        SUPERVISOR = "SUPERVISOR", 'supervisor'
        ORIENTADOR = "ORIENTADOR", 'orientador'
        ESTAGIARIO = "ESTAGIARIO", 'estagiario'

    email = models.EmailField(unique=True, verbose_name='Email')
    username = models.CharField(unique=True, verbose_name='Username', max_length=10)
    biografia = models.CharField(verbose_name='Bio', max_length=50, blank=True)
    outrasinformacoes = models.CharField(verbose_name='OutrasInformacoes', max_length=500, blank=True)
    image = models.ImageField(upload_to='pics', default='padrao.png')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    base_role = Role.SUPERVISOR
    data_final = models.DateField(verbose_name='Data Final', null=True, blank=True)
    role = models.CharField(max_length=50, choices=Role.choices)

    class Meta:
        verbose_name_plural = "Supervisor"

    def get_absolute_url(self):
        return reverse('supervisores')

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
            if self.base_role == "SUPERVISOR":
                self.set_password(self.password)
        super().save(*args, **kwargs)


class Orientador(User):
    base_role = User.Role.ORIENTADOR
    data_de_nascimento = models.DateField(verbose_name='Nascimento', blank=True)
    telefone = PhoneNumberField(verbose_name='Telefone', blank=True)

    class Meta:
        verbose_name_plural = "Orientador"


    def welcome(self):
        return "Only Orientador"

    def get_absolute_url(self):
        return reverse('orientadores')

    def save(self, *args, **kwargs):
        if not self.pk:
            self.set_password(self.password)
        super().save(*args, **kwargs)




class Estagiario(User):
    ANO_CHOICES = [
        (3, '3º Ano'),
        (4, '4º Ano'),
    ]
    base_role = User.Role.ESTAGIARIO
    ano_letivo = models.IntegerField(verbose_name='Ano', blank=True, default=3, choices=ANO_CHOICES)
    data_de_nascimento = models.DateField(verbose_name='Nascimento', blank=True)
    telefone = PhoneNumberField(verbose_name='Telefone', blank=True)
    orientador_responsavel = models.ForeignKey(Orientador, on_delete=models.SET_NULL, null=True, blank=True, related_name='estagiarios', verbose_name='Orientador')

    class Meta:
        verbose_name_plural = "Estagiario"

    def get_absolute_url(self):
        return reverse('estagiarios')
    def welcome(self):
        return "Only Estagiario"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.set_password(self.password)
        super().save(*args, **kwargs)


class Participante(models.Model):
    username = models.CharField(unique=True, verbose_name='Username', max_length=100)
    date_joined = models.DateTimeField(verbose_name='Date Joined', auto_now_add=True)
    date_final = models.DateTimeField(verbose_name='Date Final', blank=True, null=True)
    nome = models.CharField(max_length=100)
    sobrenome = models.CharField(max_length=100)
    telefone = PhoneNumberField(verbose_name='Telefone', blank=True)
    motivo_busca_atendimento = models.TextField(verbose_name='Motivo da Busca por Atendimento', blank=True)
    estagiarios = models.ManyToManyField(Estagiario, related_name='participante_profiles', blank=True)
    is_active = models.BooleanField(default=True, verbose_name='Ativo')


    def get_absolute_url(self):
        return reverse('participantes')

    def save(self, *args, **kwargs):
        self.username = f"{self.nome.replace(' ', '').capitalize()}_{self.sobrenome.replace(' ', '').capitalize()}"
        if not self.date_joined:
            self.date_joined = timezone.now()
        super().save(*args, **kwargs)
    def __str__(self):
        return self.nome


class Endereco(models.Model):
    cep = models.CharField(verbose_name='CEP', max_length=8)
    numero = models.CharField(verbose_name='Número', max_length=10)
    complemento = models.CharField(verbose_name='Complemento', max_length=255, blank=True)
    cidade = models.CharField(verbose_name='Cidade', max_length=100, blank=True)
    estado = models.CharField(verbose_name='estado', max_length=100, blank=True)
    bairro = models.CharField(verbose_name='Bairro', max_length=100, blank=True)
    av_r = models.CharField(verbose_name="AV", max_length=300,  blank=True)
    participante = models.OneToOneField(Participante, on_delete=models.CASCADE , null=True, blank=True, verbose_name='Endereço')

    def get_absolute_url(self):
        return reverse('participantes')


class Documentos(models.Model):
    titulo = models.CharField(max_length=255)
    descricao = models.CharField(max_length=255)
    data_criacao = models.DateTimeField(auto_now_add=True)
    pertence = models.ForeignKey(Participante, on_delete=models.CASCADE)
    criado_por = models.ForeignKey(User, on_delete=models.CASCADE)
    arquivo = models.FileField(upload_to='Documentos')
    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse('List_Documetos',args=[self.pertence.id] )