from django.contrib import admin
from .models import *
from .models.users import EstagiarioProfile, OrientadorProfile

# Register your models here.

admin.site.register(User)
admin.site.register(EstagiarioProfile)
admin.site.register(OrientadorProfile)