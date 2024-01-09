from django import forms
from .models.users import *

class OrientadorForm(forms.ModelForm):
    class Meta:
        model = Orientador
        fields = '__all__'
        exclude = ['role', 'user_permissions', 'groups', 'is_staff', 'is_superuser', 'last_login', 'is_active']

