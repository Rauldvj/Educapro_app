"""
Autores:
Raúl Córdova Vicencio
Francisca Olavarría Pavez
Carlos Olivero Bruno

Fecha: 01 diciembre 2024

Descripción:
Este módulo define los formularios utilizados en la aplicación para gestionar los registros del Programa de Integración Escolar (PIE). Los formularios están basados en el modelo RegistroPie y permiten listar y agregar registros de estudiantes y sus apoderados.

Formularios:
- ListPieForm: Formulario para listar los registros de PIE.
- AddRegistroPieForm: Formulario para agregar un nuevo registro de PIE.
"""

from django import forms
from .models import RegistroPie

class ListPieForm(forms.ModelForm):
    """
    Formulario para listar los registros de PIE.

    Meta:
    - model: RegistroPie
    - fields: ['estudiante', 'apoderado_titular']
    """
    class Meta:
        model = RegistroPie
        fields = ['estudiante', 'apoderado_titular']

class AddRegistroPieForm(forms.ModelForm):
    """
    Formulario para agregar un nuevo registro de PIE.

    Meta:
    - model: RegistroPie
    - fields: ['estudiante', 'apoderado_titular']
    """
    class Meta:
        model = RegistroPie
        fields = ['estudiante', 'apoderado_titular']


