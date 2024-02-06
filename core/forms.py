from django import forms
from .models.users import *
from django.contrib.auth.forms import UserChangeForm
from phonenumber_field.formfields import PhoneNumberField
from django.contrib.auth.forms import PasswordChangeForm

class OrientadorForm(forms.ModelForm):

    class Meta:
        model = Orientador
        fields = '__all__'
        exclude = ['role', 'username','user_permissions', 'groups', 'is_staff', 'is_superuser', 'last_login', 'is_active','password','image',]
        fields = [ 'first_name', 'last_name', 'email', 'data_de_nascimento', 'telefone', 'biografia','outrasinformacoes']



class OrientadorFormEdit(forms.ModelForm):
    class Meta:
        model = Orientador
        exclude = ['role','username', 'user_permissions', 'groups', 'is_staff', 'is_superuser', 'last_login', 'is_active','image']
        fields = ['first_name', 'last_name', 'data_de_nascimento', 'telefone','biografia','outrasinformacoes' ]



class EstagiarioForm(forms.ModelForm):

    class Meta:
        model = Estagiario
        fields = '__all__'
        exclude = ['role', 'username','user_permissions', 'groups', 'is_staff', 'is_superuser', 'last_login', 'is_active','password','image']
        fields = [ 'first_name', 'last_name', 'email', 'data_de_nascimento','ano_letivo', 'telefone','biografia','outrasinformacoes','orientador_responsavel']



class EstagiarioFormEdit(forms.ModelForm):
    class Meta:
        model = Estagiario
        exclude = ['role','username', 'user_permissions', 'groups', 'is_staff', 'is_superuser', 'last_login', 'is_active','image']
        fields = ['first_name', 'last_name', 'data_de_nascimento', 'telefone','orientador_responsavel','biografia','outrasinformacoes','ano_letivo']


class SupervisorForm(forms.ModelForm):

    class Meta:
        model = User
        fields = '__all__'
        exclude = ['role', 'username','user_permissions', 'groups', 'is_staff', 'is_superuser', 'last_login', 'is_active','password', 'password_confirm', 'image']
        fields = ['first_name', 'last_name', 'email','biografia','outrasinformacoes']




class SupervisorFormEdit(forms.ModelForm):
    class Meta:
        model = User
        exclude = ['role','username','user_permissions', 'groups', 'is_staff', 'is_superuser', 'last_login', 'is_active', 'image',]
        fields = ['first_name', 'last_name','biografia','outrasinformacoes',]




class ParticipanteForm(forms.ModelForm):
    class Meta:
        model = Participante
        fields = '__all__'
        exclude = ['username','date_joined','date_final', 'responsavel', 'qtd_atendimentos', 'is_active']


class ResponsavelForm(forms.ModelForm):
    class Meta:
        model = Responsavel
        fields = '__all__'
        exclude = ['participante']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.required = False

class EnderecoForm(forms.ModelForm):
    class Meta:
        model = Endereco
        fields = '__all__'
        exclude = ['participante']

    widgets = {
        'cep': forms.TextInput(attrs={'class': 'cep-input'}),
    }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        exclude = ['role', 'user_permissions', 'groups', 'is_staff', 'is_superuser', 'last_login', 'is_active', 'image', 'password','date_joined','data_final','username']

class OrientadorEditProfileForm(UserChangeForm):
    telefone = PhoneNumberField(label='Telefone', required=False)
    data_de_nascimento = forms.DateField(label='Data de Nascimento', required=False)

    class Meta:
        model = Orientador
        fields = ['first_name', 'last_name', 'telefone', 'biografia', 'outrasinformacoes', 'data_de_nascimento']