from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import time
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField
import secrets
import string
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
    biografia = models.CharField(verbose_name='Biografia', max_length=50, blank=True)
    outrasinformacoes = models.CharField(verbose_name='Outras Informações', max_length=500, blank=True)
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
        if not self.username:
            self.username = f"{self.first_name.replace(' ', '-')}-{self.last_name.replace(' ', '-')}"
        if not self.pk:
            self.role = self.base_role
            generated_password = secrets.token_urlsafe(6)
            self.set_password(generated_password)
        super().save(*args, **kwargs)


class Orientador(User):
    base_role = User.Role.ORIENTADOR
    data_de_nascimento = models.DateField(verbose_name='Data De Nascimento', blank=True)
    telefone = models.CharField(verbose_name='Telefone', blank=True, max_length=16)

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
    telefone = models.CharField(verbose_name='Telefone', blank=True,  max_length=16)
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
    telefone = models.CharField(verbose_name='Telefone', blank=True, null=True,  max_length=16)
    motivo_busca_atendimento = models.TextField(verbose_name='Motivo da Busca por Atendimento', blank=True)
    data_de_nascimento = models.DateField( blank=True, null=True)
    escola = models.CharField(max_length=100,blank=True, null=True)
    serie = models.IntegerField(verbose_name='serie', blank=True, null=True)

    is_active = models.BooleanField(default=True, verbose_name='Ativo')
    qtd_atendimentos = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('Participante_perfil', kwargs={'username': self.username})

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = f"{self.nome.replace(' ', '-')}-{self.sobrenome.replace(' ', '-')}"
        if not self.date_joined:
            self.date_joined = timezone.now()

        super().save(*args, **kwargs)
    def __str__(self):
        return self.nome


class Responsavel(models.Model):

    nome = models.CharField(max_length=100)
    sobrenome = models.CharField(max_length=100)
    telefone = models.CharField(verbose_name='Telefone', blank=True, null=True,  max_length=16)
    email = models.EmailField()
    participante = models.OneToOneField(Participante, blank=True, null=True, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('participantes')


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
        return reverse('Participante_perfil', kwargs={'username': self.participante.username})



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


class agenda(models.Model):
    SEMANA_CHOICES = [
        (0, 'SEGUNDA-FEIRA'),
        (1, 'TERÇA-FEIRA'),
        (2, 'QUARTA-FEIRA'),
        (3, 'QUINTA-FEIRA'),
        (4, 'SEXTA-FEIRA'),
        (5, 'SÁBADO'),
        (6, 'DOMINGO'),
    ]

    HORARIO_CHOICES = [
        (time(8, 10), '8:10'),
        (time(9, 10), '9:10'),
        (time(10, 10), '10:10'),
        (time(11, 10), '11:10'),
        (time(12, 10), '12:10'),
        (time(13, 10), '13:10'),
        (time(14, 10), '14:10'),
        (time(15, 10), '15:10'),
        (time(16, 10), '16:10'),
        (time(17, 10), '17:10'),

    ]

    dia_da_semana = models.IntegerField(verbose_name='Semana', blank=True, choices=SEMANA_CHOICES)
    horario = models.TimeField(choices=HORARIO_CHOICES)
    participante = models.OneToOneField(Participante, on_delete=models.CASCADE, null=True, blank=True ,related_name='agendas_participante')
    estagiario = models.ManyToManyField(Estagiario,  null=True, blank=True, related_name='agendas_estagiario')
    reservadoPor = models.ForeignKey(User, on_delete=models.SET_NULL,  null=True, blank=True)

    def clean(self):
        existing_record = agenda.objects.filter(dia_da_semana=self.dia_da_semana, horario=self.horario).exclude(
            pk=self.pk).first()
        if existing_record:
            raise ValidationError(
                f"Já existe um registro para o dia {self.get_dia_da_semana_display()} e horário {self.horario}.")


    def __str__(self):
        return f"{self.get_dia_da_semana_display()}"



class Atendimentos(models.Model):
    participante = models.ForeignKey(Participante, on_delete=models.CASCADE)
    estagiario = models.ManyToManyField(Estagiario, related_name='atendimentos')
    data_atendimento = models.DateTimeField(verbose_name='Data do Atendimento')
    motivoFalta = models.CharField(max_length=100, verbose_name='Motivo da Falta', null=True, blank=True)
    presenca = models.BooleanField(default=False)
    ocorreu = models.BooleanField(default=False)


class UserActivity(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    last_activity = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username}"
    def update_activity(self):
        self.last_activity = timezone.now()
        self.save()