from django import forms
from .models.users import *
from django.contrib.auth.forms import UserChangeForm
from phonenumber_field.formfields import PhoneNumberField
from django.contrib.auth.forms import PasswordChangeForm

class OrientadorForm(forms.ModelForm):
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='Confirme a Senha')

    class Meta:
        model = Orientador
        fields = '__all__'
        exclude = ['role', 'user_permissions', 'groups', 'is_staff', 'is_superuser', 'last_login', 'is_active']
        fields = ['username', 'password', 'password_confirm', 'first_name', 'last_name', 'email', 'data_de_nascimento', 'telefone', 'biografia','outrasinformacoes','image', 'role']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")


        if password and password_confirm and password != password_confirm:
            self.add_error('password', forms.ValidationError("As senhas não coincidem."))
            self.add_error('password_confirm', forms.ValidationError("As senhas não coincidem."))






class OrientadorFormEdit(forms.ModelForm):
    class Meta:
        model = Orientador
        exclude = ['role', 'user_permissions', 'groups', 'is_staff', 'is_superuser', 'last_login', 'is_active']
        fields = ['username', 'first_name', 'last_name', 'data_de_nascimento', 'telefone','biografia','outrasinformacoes', 'image']



class EstagiarioForm(forms.ModelForm):
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='Confirme a Senha')

    class Meta:
        model = Estagiario
        fields = '__all__'
        exclude = ['role', 'user_permissions', 'groups', 'is_staff', 'is_superuser', 'last_login', 'is_active']
        fields = ['username', 'password', 'password_confirm', 'first_name', 'last_name', 'email', 'data_de_nascimento','ano_letivo', 'telefone','biografia','outrasinformacoes','orientador_responsavel', 'image']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("As senhas não coincidem. Por favor, tente novamente.")


class EstagiarioFormEdit(forms.ModelForm):
    class Meta:
        model = Estagiario
        exclude = ['role', 'user_permissions', 'groups', 'is_staff', 'is_superuser', 'last_login', 'is_active']
        fields = ['username', 'first_name', 'last_name', 'data_de_nascimento', 'telefone','orientador_responsavel','biografia','outrasinformacoes','ano_letivo','image']


class SupervisorForm(forms.ModelForm):
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='Confirme a Senha')

    class Meta:
        model = User
        fields = '__all__'
        exclude = ['role', 'user_permissions', 'groups', 'is_staff', 'is_superuser', 'last_login', 'is_active']
        fields = ['username', 'password', 'password_confirm', 'first_name', 'last_name', 'email','biografia','outrasinformacoes', 'image', 'role']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("As senhas não coincidem. Por favor, tente novamente.")


class SupervisorFormEdit(forms.ModelForm):
    class Meta:
        model = User
        exclude = ['role', 'user_permissions', 'groups', 'is_staff', 'is_superuser', 'last_login', 'is_active']
        fields = ['username', 'first_name', 'last_name','biografia','outrasinformacoes', 'image',]


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