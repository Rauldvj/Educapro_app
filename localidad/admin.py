from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Region)

class ComunaAdmin(admin.ModelAdmin):
    list_display = ['region', 'comuna']
    search_fields = ['comuna']
admin.site.register(Comuna, ComunaAdmin)