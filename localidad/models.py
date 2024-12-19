"""
Autores:
Raúl Córdova Vicencio
Francisca Olavarría Pavez
Carlos Olivero Bruno

Fecha: 01 diciembre 2024

Descripción:
Este módulo define los modelos de datos para la gestión de localidades en la aplicación. Incluye modelos para representar regiones y comunas, permitiendo una estructura jerárquica donde cada comuna pertenece a una región específica. Estos modelos son fundamentales para organizar y categorizar la información geográfica relacionada con los estudiantes y sus apoderados.

Modelos:
- Region: Representa una región geográfica.
- Comuna: Representa una comuna, que está asociada a una región específica.
"""

from django.db import models

# Create your models here.

#____________________________________________________________________________________________________________
# MODELO REGION 
class Region(models.Model):
    """
    Modelo que representa una región geográfica.

    Atributos:
    - region: Nombre de la región.
    """
    region = models.CharField(max_length=100, verbose_name='Region')
    
    def __str__(self):
        return self.region
        
#____________________________________________________________________________________________________________

# MODELO COMUNA QUE HEREDA LA REGION DEL MODELO "REGION"
class Comuna(models.Model):
    """
    Modelo que representa una comuna, asociada a una región específica.

    Atributos:
    - comuna: Nombre de la comuna.
    - region: Región a la que pertenece la comuna.
    """
    comuna = models.CharField(max_length=100, verbose_name='Comuna')
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.comuna}'

