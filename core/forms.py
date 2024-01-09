from django import forms
from .models.users import *

class OrientadorForm(forms.ModelForm):
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='Confirme a Senha')

    class Meta:
        model = Orientador
        fields = '__all__'
        exclude = ['role', 'user_permissions', 'groups', 'is_staff', 'is_superuser', 'last_login', 'is_active']
        fields = ['username', 'password', 'password_confirm', 'first_name', 'last_name', 'email', 'data_de_nascimento', 'telefone', 'image', 'role']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("As senhas não coincidem. Por favor, tente novamente.")

