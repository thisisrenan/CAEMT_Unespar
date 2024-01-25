from django.contrib import admin

from .models.users import *

# Register your models here.

admin.site.register(User)
admin.site.register(Estagiario)
admin.site.register(Orientador)
admin.site.register(Participante)
admin.site.register(Documentos)
admin.site.register(Endereco)
admin.site.register(agenda)