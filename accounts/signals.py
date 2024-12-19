"""
Autores:
- Raúl Córdova Vicencio
- Francisca Olavarría Pavez
- Carlos Olivero Bruno
Fecha: 01 diciembre 2024
"""

from django.contrib.auth.models import Group
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from .models import Profile

@receiver(post_save, sender=Profile)
def add_user_to_funcionarios_group(sender, instance, created, **kwargs):
    """
    Agrega al usuario al grupo 'Funcionarios' cuando se crea un perfil.
    Si el grupo no existe, lo crea junto con otros grupos predeterminados.
    
    Args:
        sender (Model): El modelo que envía la señal.
        instance (Profile): La instancia del perfil.
        created (bool): Indica si el perfil fue creado.
        **kwargs: Argumentos adicionales.
    """
    if created:
        try:
            group1 = Group.objects.get(name='Funcionarios')
        except Group.DoesNotExist:
            group1 = Group.objects.create(name='Funcionarios')
            group2 = Group.objects.create(name='Administradores')
            group3 = Group.objects.create(name='Coordinadores')
            group4 = Group.objects.create(name='Coordinadores Suplentes')
            group5 = Group.objects.create(name='Educadores Diferenciales')
            group6 = Group.objects.create(name='Psicopedagógos')
            group7 = Group.objects.create(name='Psicólogos')
            group8 = Group.objects.create(name='Terapeutas Ocupacionales')
            group9 = Group.objects.create(name='Fonoaudiologos')
            group10 = Group.objects.create(name='Técnicos Diferenciales')
            group11 = Group.objects.create(name='Técnicos Parvularios')
        instance.user.groups.add(group1)