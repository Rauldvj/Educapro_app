"""
Autores:
- Raúl Córdova Vicencio
- Francisca Olavarría Pavez
- Carlos Olivero Bruno
Fecha: 01 diciembre 2024
"""

from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Profile

# Define una clase inline para el perfil del usuario
class ProfileInline(admin.StackedInline):
    """
    Clase para agregar el perfil del usuario como un inline en el admin de Django.
    
    Atributos:
        model (Profile): El modelo relacionado.
        can_delete (bool): Indica si el perfil puede ser eliminado.
        verbose_name_plural (str): Nombre plural para el perfil.
        fields (tuple): Campos a mostrar en el inline.
    """
    model = Profile
    can_delete = False
    verbose_name_plural = 'perfiles'
    fields = ('image', 'rut', 'direccion', 'region', 'comuna', 'telefono', 
              'apellido_paterno', 'apellido_materno', 'creado_por_coordinador')

# Define una clase personalizada para el modelo de administración del usuario
class UserAdmin(BaseUserAdmin):
    """
    Clase personalizada para la administración de usuarios en el admin de Django.
    
    Atributos:
        inlines (tuple): Inlines a incluir en el admin.
        list_display (tuple): Campos a mostrar en la lista de usuarios.
        list_filter (tuple): Filtros a aplicar en la lista de usuarios.
        search_fields (tuple): Campos por los cuales se puede buscar.
        ordering (tuple): Orden de los usuarios.
        fieldsets (tuple): Secciones y campos a mostrar en el formulario de usuario.
    """
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'email')
    ordering = ('username',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información personal', {'fields': ('first_name', 'email')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas importantes', {'fields': ('last_login', 'date_joined')}),
    )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Define una clase personalizada para el modelo de administración del perfil
class ProfileAdmin(admin.ModelAdmin):
    """
    Clase personalizada para la administración de perfiles en el admin de Django.
    
    Atributos:
        list_display (tuple): Campos a mostrar en la lista de perfiles.
        search_fields (tuple): Campos por los cuales se puede buscar.
        list_filter (tuple): Filtros a aplicar en la lista de perfiles.
    """
    list_display = ('user', 'apellido_paterno', 'apellido_materno', 'rut', 
                    'direccion', 'region', 'comuna', 'telefono', 'creado_por_coordinador')
    search_fields = ('rut', 'user__username', 'apellido_paterno', 'apellido_materno')
    list_filter = ('region', 'comuna', 'creado_por_coordinador')

admin.site.register(Profile, ProfileAdmin)
