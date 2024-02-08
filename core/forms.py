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

    telefone = PhoneNumberField(
        widget=forms.TextInput(attrs={'class': 'telefone-input', 'placeholder': '+55 (__) 9 9999 9999'}),
        error_messages={'invalid': 'Número de telefone inválido'}
    )
    data_de_nascimento = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'data-nascimento-input', 'placeholder': 'DD/MM/AAAA'}),
        error_messages={'invalid': 'Data de nascimento inválida'}
    )
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'class': 'email-input', 'placeholder': 'email@gmail.com'}),
        error_messages={'invalid': 'Email inválido'}
    )



class OrientadorFormEdit(forms.ModelForm):
    class Meta:
        model = Orientador
        exclude = ['role','username', 'user_permissions', 'groups', 'is_staff', 'is_superuser', 'last_login', 'is_active','image']
        fields = ['first_name', 'last_name', 'data_de_nascimento', 'telefone','biografia','outrasinformacoes' ]

    telefone = PhoneNumberField(
        widget=forms.TextInput(attrs={'class': 'telefone-input', 'placeholder': '+55 (__) 9 9999 9999'}),
        error_messages={'invalid': 'Número de telefone inválido'}
    )
    data_de_nascimento = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'data-nascimento-input', 'placeholder': 'DD/MM/AAAA'}),
        error_messages={'invalid': 'Data de nascimento inválida'}
    )



class EstagiarioForm(forms.ModelForm):

    class Meta:
        model = Estagiario
        fields = '__all__'
        exclude = ['role', 'username','user_permissions', 'groups', 'is_staff', 'is_superuser', 'last_login', 'is_active','password','image']
        fields = [ 'first_name', 'last_name', 'email', 'data_de_nascimento','ano_letivo', 'telefone','biografia','outrasinformacoes','orientador_responsavel']

    telefone = PhoneNumberField(
        widget=forms.TextInput(attrs={'class': 'telefone-input', 'placeholder': '+55 (__) 9 9999 9999'}),
        error_messages={'invalid': 'Número de telefone inválido'}
    )
    data_de_nascimento = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'data-nascimento-input', 'placeholder': 'DD/MM/AAAA'}),
        error_messages={'invalid': 'Data de nascimento inválida'}
    )
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'class': 'email-input', 'placeholder': 'email@gmail.com'}),
        error_messages={'invalid': 'Email inválido'}
    )


class EstagiarioFormEdit(forms.ModelForm):
    class Meta:
        model = Estagiario
        exclude = ['role','username', 'user_permissions', 'groups', 'is_staff', 'is_superuser', 'last_login', 'is_active','image']
        fields = ['first_name', 'last_name', 'data_de_nascimento', 'telefone','orientador_responsavel','biografia','outrasinformacoes','ano_letivo']

    telefone = PhoneNumberField(
        widget=forms.TextInput(attrs={'class': 'telefone-input', 'placeholder': '+55 (__) 9 9999 9999'}),
        error_messages={'invalid': 'Número de telefone inválido'}
    )
    data_de_nascimento = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'data-nascimento-input', 'placeholder': 'DD/MM/AAAA'}),
        error_messages={'invalid': 'Data de nascimento inválida'}
    )


class SupervisorForm(forms.ModelForm):

    class Meta:
        model = User
        fields = '__all__'
        exclude = ['role', 'username','user_permissions', 'groups', 'is_staff', 'is_superuser', 'last_login', 'is_active','password', 'password_confirm', 'image']
        fields = ['first_name', 'last_name', 'email','biografia','outrasinformacoes']

    telefone = PhoneNumberField(
        widget=forms.TextInput(attrs={'class': 'telefone-input', 'placeholder': '+55 (__) 9 9999 9999'}),
        error_messages={'invalid': 'Número de telefone inválido'}
    )
    data_de_nascimento = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'data-nascimento-input', 'placeholder': 'DD/MM/AAAA'}),
        error_messages={'invalid': 'Data de nascimento inválida'}
    )
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'class': 'email-input', 'placeholder': 'email@gmail.com'}),
        error_messages={'invalid': 'Email inválido'}
    )


class SupervisorFormEdit(forms.ModelForm):
    class Meta:
        model = User
        exclude = ['role','username','user_permissions', 'groups', 'is_staff', 'is_superuser', 'last_login', 'is_active', 'image',]
        fields = ['first_name', 'last_name','biografia','outrasinformacoes',]

    telefone = PhoneNumberField(
        widget=forms.TextInput(attrs={'class': 'telefone-input', 'placeholder': '+55 (__) 9 9999 9999'}),
        error_messages={'invalid': 'Número de telefone inválido'}
    )
    data_de_nascimento = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'data-nascimento-input', 'placeholder': 'DD/MM/AAAA'}),
        error_messages={'invalid': 'Data de nascimento inválida'}
    )



class ParticipanteForm(forms.ModelForm):
    class Meta:
        model = Participante
        fields = '__all__'
        exclude = ['username','date_joined','date_final', 'responsavel', 'qtd_atendimentos', 'is_active']

    telefone = PhoneNumberField(
        widget=forms.TextInput(attrs={'class': 'telefone-input', 'placeholder': '+55 (__) 9 9999 9999'}),
        error_messages={'invalid': 'Número de telefone inválido'}
    )
    data_de_nascimento = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'data-nascimento-input', 'placeholder': 'DD/MM/AAAA'}),
        error_messages={'invalid': 'Data de nascimento inválida'}
    )


class ResponsavelForm(forms.ModelForm):
    class Meta:
        model = Responsavel
        fields = '__all__'
        exclude = ['participante']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.required = False

    telefone = PhoneNumberField(
        widget=forms.TextInput(attrs={'class': 'telefone-input', 'placeholder': '+55 (__) 9 9999 9999'}),
        error_messages={'invalid': 'Número de telefone inválido'}
    )

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

    telefone = PhoneNumberField(
        widget=forms.TextInput(attrs={'class': 'telefone-input', 'placeholder': '+55 (__) 9 9999 9999'}),
        error_messages={'invalid': 'Número de telefone inválido'}
    )
    data_de_nascimento = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'data-nascimento-input', 'placeholder': 'DD/MM/AAAA'}),
        error_messages={'invalid': 'Data de nascimento inválida'}
    )

class OrientadorEditProfileForm(UserChangeForm):
    telefone = PhoneNumberField(label='Telefone', required=False)
    data_de_nascimento = forms.DateField(label='Data de Nascimento', required=False)

    class Meta:
        model = Orientador
        fields = ['first_name', 'last_name', 'telefone', 'biografia', 'outrasinformacoes', 'data_de_nascimento']

    telefone = PhoneNumberField(
        widget=forms.TextInput(attrs={'class': 'telefone-input', 'placeholder': '+55 (__) 9 9999 9999'}),
        error_messages={'invalid': 'Número de telefone inválido'}
    )
    data_de_nascimento = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'data-nascimento-input', 'placeholder': 'DD/MM/AAAA'}),
        error_messages={'invalid': 'Data de nascimento inválida'}
    )

class inputImage(UserChangeForm):
    class Meta:
        model = User
        fields = ['image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget = forms.ClearableFileInput(attrs={'class': 'form-control'})