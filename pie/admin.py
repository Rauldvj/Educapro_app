"""
Autores:
Raúl Córdova Vicencio
Francisca Olavarría Pavez
Carlos Olivero Bruno

Fecha: 01 diciembre 2024

Descripción:
Este módulo configura la interfaz de administración de Django para el modelo RegistroPie. Define cómo se muestran y gestionan los registros de PIE (Programa de Integración Escolar) en el panel de administración, incluyendo la disposición de los campos y las opciones de visualización.

Modelos Administrados:
- RegistroPie: Modelo que representa el registro de un estudiante en el Programa de Integración Escolar.

Configuraciones de Administración:
- RegistroPieAdmin: Configuración personalizada para la administración del modelo RegistroPie.
"""

from django.contrib import admin
from .models import RegistroPie

class RegistroPieAdmin(admin.ModelAdmin):
    """
    Configuración de la interfaz de administración para el modelo RegistroPie.

    Atributos:
    - list_display: Campos que se mostrarán en la lista de registros.
    - fieldsets: Disposición de los campos en el formulario de edición.
    """
    list_display = ('año_registro', 'curso', 'estudiante', 'apoderado_titular')  # Campos mostrados en la lista de registros
    
    fieldsets = (
        ('Datos del Estudiante', {
            'fields': ('estudiante', 'apoderado_titular')
        }),
        ('Datos de la Matricula', {
            'fields': ('año_registro', 'curso', 'enable')
        }),
    )

# Registro del modelo RegistroPie en la interfaz de administración
admin.site.register(RegistroPie, RegistroPieAdmin)