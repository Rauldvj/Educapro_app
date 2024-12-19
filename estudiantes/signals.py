"""
Autores:
Raúl Córdova Vicencio
Francisca Olavarría Pavez
Carlos Olivero Bruno
Fecha: 01 diciembre 2024

Este módulo contiene señales de Django para manejar la creación, actualización y eliminación de informes y registros
relacionados con los estudiantes. Las señales se utilizan para automatizar la creación y actualización de instancias
de modelos relacionados cuando se crean, actualizan o eliminan instancias de estudiantes.
"""

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta, date
from estudiantes.models import Estudiante, ApoderadoTitular, BitacoraEstudiante, PromedioDia, PromedioSemanalHistorico, PromedioMensualHistorico
from pie.models import RegistroPie
from .models import AnamnesisEstudiante, Familiar, Profile, Pai, Paci

#_____________________________________________________________________________________________________________
# SIGNALS PARA CREAR O ACTUALIZAR LOS INFORMES DE ANAMNESIS, PAI Y PACI

def calcular_edad(fecha_nacimiento):
    """
    Calcula la edad de una persona basada en su fecha de nacimiento.
    
    :param fecha_nacimiento: Fecha de nacimiento de la persona.
    :return: Edad de la persona en años.
    """
    today = date.today()
    return today.year - fecha_nacimiento.year - ((today.month, today.day) < (fecha_nacimiento.month, fecha_nacimiento.day))

@receiver(post_save, sender=Estudiante)
def crear_actualizar_informes(sender, instance, created, **kwargs):
    """
    Crea o actualiza los informes de Anamnesis, PAI y PACI cuando se crea o actualiza una instancia de Estudiante.
    
    :param sender: El modelo que envía la señal.
    :param instance: La instancia del modelo que envía la señal.
    :param created: Booleano que indica si la instancia fue creada (True) o actualizada (False).
    """
    edad = calcular_edad(instance.fecha_nacimiento) if instance.fecha_nacimiento else None
    if created:
        # Crear una nueva instancia de AnamnesisEstudiante
        AnamnesisEstudiante.objects.create(
            estudiante=instance,
            curso_actual=instance.cursos,
            edad=edad
        )
        # Crear una nueva instancia de Pai
        Pai.objects.create(
            estudiante=instance,
            curso=instance.cursos,
            edad=edad
        )
        # Crear una nueva instancia de Paci
        Paci.objects.create(
            estudiante=instance,
            curso=instance.cursos,
            edad=edad
        )
    else:
        # Actualizar la instancia existente de AnamnesisEstudiante
        anamnesis = AnamnesisEstudiante.objects.filter(estudiante=instance).first()
        if anamnesis:
            anamnesis.curso_actual = instance.cursos
            anamnesis.edad = edad
            anamnesis.save()
        # Actualizar la instancia existente de Pai
        pai = Pai.objects.filter(estudiante=instance).first()
        if pai:
            pai.curso = instance.cursos
            pai.edad = edad
            pai.save()
        # Actualizar la instancia existente de Paci
        paci = Paci.objects.filter(estudiante=instance).first()
        if paci:
            paci.curso = instance.cursos
            paci.edad = edad
            paci.save()

@receiver(post_delete, sender=Estudiante)
def eliminar_informes(sender, instance, **kwargs):
    """
    Elimina los informes de Anamnesis, PAI y PACI cuando se elimina una instancia de Estudiante.
    
    :param sender: El modelo que envía la señal.
    :param instance: La instancia del modelo que envía la señal.
    """
    # Eliminar la instancia de AnamnesisEstudiante asociada
    AnamnesisEstudiante.objects.filter(estudiante=instance).delete()
    # Eliminar la instancia de Pai asociada
    Pai.objects.filter(estudiante=instance).delete()
    # Eliminar la instancia de Paci asociada
    Paci.objects.filter(estudiante=instance).delete()

#_____________________________________________________________________________________________________________
# SIGNALS PARA ACTUALIZAR EL REGISTRO PIE Y EL APODERADO TITULAR

@receiver(post_save, sender=Estudiante)
def crear_registro_estudiante_pie(sender, instance, created, **kwargs):
    """
    Crea o actualiza el registro PIE y el apoderado titular cuando se crea o actualiza una instancia de Estudiante.
    
    :param sender: El modelo que envía la señal.
    :param instance: La instancia del modelo que envía la señal.
    :param created: Booleano que indica si la instancia fue creada (True) o actualizada (False).
    """
    if created:
        # Verifica si ya existen instancias antes de crearlas
        if not ApoderadoTitular.objects.filter(estudiante=instance).exists():
            ApoderadoTitular.objects.create(estudiante=instance)

        if not RegistroPie.objects.filter(estudiante=instance).exists():
            RegistroPie.objects.create(estudiante=instance, curso=instance.cursos)
    else:
        # Actualiza el campo curso en RegistroPie si el estudiante ya existe
        registro_pie = RegistroPie.objects.filter(estudiante=instance).first()
        if registro_pie:
            registro_pie.curso = instance.cursos
            registro_pie.save()

@receiver(post_save, sender=ApoderadoTitular)
def actualizar_apoderado_titular_registro_pie(sender, instance, **kwargs):
    """
    Actualiza el apoderado titular en el registro PIE cuando se crea o actualiza una instancia de ApoderadoTitular.
    
    :param sender: El modelo que envía la señal.
    :param instance: La instancia del modelo que envía la señal.
    """
    try:
        registro_pie = RegistroPie.objects.get(estudiante=instance.estudiante)
        registro_pie.apoderado_titular = instance  # Actualiza el apoderado titular
        registro_pie.save()  # Guarda los cambios en el registro PIE
    except RegistroPie.DoesNotExist:
        pass  # Si no existe un registro PIE, no hace nada

#_____________________________________________________________________________________________________________

@receiver(post_save, sender=BitacoraEstudiante)
def actualizar_promedios(sender, instance, **kwargs):
    """
    Actualiza los promedios diarios, semanales y mensuales históricos cuando se crea o actualiza una instancia de BitacoraEstudiante.
    
    :param sender: El modelo que envía la señal.
    :param instance: La instancia del modelo que envía la señal.
    """
    # Actualiza el promedio diario
    promedio_dia, created = PromedioDia.objects.get_or_create(estudiante=instance.estudiante, bitacora=instance)
    promedio_dia.save()
    
    # Actualiza el promedio semanal histórico
    inicio_semana = instance.fecha - timedelta(days=instance.fecha.weekday())
    fin_semana = inicio_semana + timedelta(days=4)
    inicio_mes = instance.fecha.replace(day=1)
    fin_mes = (inicio_mes + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    inicio_semana = max(inicio_semana, inicio_mes)
    fin_semana = min(fin_semana, fin_mes)
    promedio_semanal_historico, created = PromedioSemanalHistorico.objects.get_or_create(
        estudiante=instance.estudiante,
        inicio_semana=inicio_semana,
        fin_semana=fin_semana
    )
    promedio_semanal_historico.promedio_semana = promedio_semanal_historico.calcular_promedio_semana()
    promedio_semanal_historico.save()
    
    # Actualiza el promedio mensual histórico
    promedio_mensual_historico, created = PromedioMensualHistorico.objects.get_or_create(
        estudiante=instance.estudiante,
        inicio_mes=inicio_mes,
        fin_mes=fin_mes
    )
    promedio_mensual_historico.promedio_mes = promedio_mensual_historico.calcular_promedio_mes()
    promedio_mensual_historico.save()

@receiver(post_delete, sender=BitacoraEstudiante)
def eliminar_promedios(sender, instance, **kwargs):
    """
    Elimina y actualiza los promedios diarios, semanales y mensuales históricos cuando se elimina una instancia de BitacoraEstudiante.
    
    :param sender: El modelo que envía la señal.
    :param instance: La instancia del modelo que envía la señal.
    """
    # Elimina el promedio diario
    PromedioDia.objects.filter(estudiante=instance.estudiante, bitacora=instance).delete()
    
    # Actualiza el promedio semanal histórico
    inicio_semana = instance.fecha - timedelta(days=instance.fecha.weekday())
    fin_semana = inicio_semana + timedelta(days=4)
    inicio_mes = instance.fecha.replace(day=1)
    fin_mes = (inicio_mes + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    inicio_semana = max(inicio_semana, inicio_mes)
    fin_semana = min(fin_semana, fin_mes)
    promedio_semanal_historico = PromedioSemanalHistorico.objects.filter(
        estudiante=instance.estudiante,
        inicio_semana=inicio_semana,
        fin_semana=fin_semana
    ).first()
    if promedio_semanal_historico:
        promedio_semanal_historico.promedio_semana = promedio_semanal_historico.calcular_promedio_semana()
        promedio_semanal_historico.save()
    
    # Actualiza el promedio mensual histórico
    promedio_mensual_historico = PromedioMensualHistorico.objects.filter(
        estudiante=instance.estudiante,
        inicio_mes=inicio_mes,
        fin_mes=fin_mes
    ).first()
    if promedio_mensual_historico:
        promedio_mensual_historico.promedio_mes = promedio_mensual_historico.calcular_promedio_mes()
        promedio_mensual_historico.save()