from django import forms
from .models.users import *

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
            raise forms.ValidationError("As senhas não coincidem. Por favor, tente novamente.")


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
        exclude = ['estagiarios','username']

class EnderecoForm(forms.ModelForm):
    class Meta:
        model = Endereco
        fields = '__all__'
        exclude = ['participante']

    widgets = {
        'cep': forms.TextInput(attrs={'class': 'cep-input'}),
    }
