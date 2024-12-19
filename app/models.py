"""
Autores:
- Raúl Córdova Vicencio
- Francisca Olavarría Pavez
- Carlos Olivero Bruno
Fecha: 01 diciembre 2024
"""

from django.db import models
from estudiantes.models import Estudiante
from django.db.models.signals import pre_save
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import Group #Importamos los Groups de Autenticación
from accounts.models import User
from estudiantes.models import *
from .opciones import *


#AQUÍ CREAREMOS LOS MODELOS PARA NUESTRA APLICACIÓN


#___________________________________________________________________________________________________________________
#MODELOS ABSTRACTOS PARA REGISTRO DE ANAMNESIS

#Modelo para Registrar un Anamnesis
class LenguaMaterna(models.Model):
    """
    Modelo para registrar la lengua materna de un estudiante.
    """
    lengua_materna = models.CharField(max_length=20, choices=opciones_lengua, default='Seleccione', verbose_name='Lengua Materna:')
    comprende_materna = models.BooleanField(max_length=10, default=False, verbose_name='Comprende:', blank=True)
    habla_materna = models.BooleanField(max_length=10, default=False, verbose_name='Habla:', blank=True)
    lee_materna = models.BooleanField(max_length=10, default=False, verbose_name='Lee:', blank=True)
    escribe_materna = models.BooleanField(max_length=10, default=False, verbose_name='Escribe:', blank=True)
    class Meta:
        abstract = True

class LenguaUso(models.Model):
    """
    Modelo para registrar la lengua de uso de un estudiante.
    """
    lengua_uso = models.CharField(max_length=20, choices=opciones_lengua, default='Seleccione', verbose_name='Lengua Uso:', blank=True)
    comprende_uso = models.BooleanField(max_length=10, default=False, verbose_name='Comprende:', blank=True)
    habla_uso = models.BooleanField(max_length=10, default=False, verbose_name='Habla:', blank=True)
    lee_uso = models.BooleanField(max_length=10, default=False, verbose_name='Lee:',blank=True)
    escribe_uso = models.BooleanField(max_length=10, default=False, verbose_name='Escribe:', blank=True)
    class Meta:
        abstract = True


    
#___________________________________________________________________________________________________________________


