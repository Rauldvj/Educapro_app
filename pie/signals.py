"""
Autores:
Raúl Córdova Vicencio
Francisca Olavarría Pavez
Carlos Olivero Bruno

Fecha: 01 diciembre 2024

Descripción:
Este módulo define las señales para la aplicación del Programa de Integración Escolar (PIE). Las señales permiten la creación y actualización automática de registros relacionados cuando se guardan instancias de ciertos modelos. Esto asegura que la información esté sincronizada y actualizada en todo momento.

Señales:
- crear_o_actualizar_registro_pie: Crea o actualiza un registro de PIE cuando se guarda una instancia de Estudiante.
- actualizar_apoderado_titular_registro_pie: Actualiza el apoderado titular en el registro de PIE cuando se guarda una instancia de ApoderadoTitular.
- actualizar_avance: Actualiza los objetivos semanales cuando se guarda una instancia de BitacoraEstudiante.
"""

import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from estudiantes.models import Estudiante, ApoderadoTitular, BitacoraEstudiante, ObjetivoSemanal
from pie.models import RegistroPie
from app.models import Anamnesis

@receiver(post_save, sender=Estudiante)
def crear_o_actualizar_registro_pie(sender, instance, created, **kwargs):
    """
    Crea o actualiza un registro de PIE cuando se guarda una instancia de Estudiante.

    Parámetros:
    - sender: El modelo que envía la señal.
    - instance: La instancia del modelo que se guarda.
    - created: Booleano que indica si la instancia fue creada.
    - kwargs: Argumentos adicionales.
    """
    if created:
        # Crear un nuevo RegistroPie cuando se crea un nuevo estudiante
        RegistroPie.objects.create(
            estudiante=instance,
            curso=instance.cursos,
            enable=instance.enable,
            año_matricula=datetime.now().year  # Registrar el año de creación
        )
    else:
        # Actualizar los campos en RegistroPie si el estudiante ya existe
        registro_pie = RegistroPie.objects.filter(estudiante=instance).first()
        if registro_pie:
            registro_pie.curso = instance.cursos
            registro_pie.enable = instance.enable
            registro_pie.save()

# -------------------------------------------------------------------------------------------------
# Actualizar registros en simultaneo con el registro PIE del Apoderado Titular

@receiver(post_save, sender=ApoderadoTitular)
def actualizar_apoderado_titular_registro_pie(sender, instance, **kwargs):
    """
    Actualiza el apoderado titular en el registro de PIE cuando se guarda una instancia de ApoderadoTitular.

    Parámetros:
    - sender: El modelo que envía la señal.
    - instance: La instancia del modelo que se guarda.
    - kwargs: Argumentos adicionales.
    """
    try:
        registro_pie = RegistroPie.objects.get(estudiante=instance.estudiante)
        registro_pie.apoderado_titular = instance  # Actualiza el apoderado titular
        registro_pie.save()  # Guarda los cambios en el registro PIE
    except RegistroPie.DoesNotExist:
        pass  # Si no existe un registro PIE, no hace nada

# -------------------------------------------------------------------------------------------------

@receiver(post_save, sender=BitacoraEstudiante)
def actualizar_avance(sender, instance, **kwargs):
    """
    Actualiza los objetivos semanales cuando se guarda una instancia de BitacoraEstudiante.

    Parámetros:
    - sender: El modelo que envía la señal.
    - instance: La instancia del modelo que se guarda.
    - kwargs: Argumentos adicionales.
    """
    objetivos = ObjetivoSemanal.objects.filter(bitacora=instance)
    for objetivo in objetivos:
        objetivo.save()