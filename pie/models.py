"""
Autores:
Raúl Córdova Vicencio
Francisca Olavarría Pavez
Carlos Olivero Bruno

Fecha: 01 diciembre 2024

Descripción:
Este módulo define el modelo de datos para el Programa de Integración Escolar (PIE) en la aplicación. El modelo RegistroPie se utiliza para registrar la información de los estudiantes que participan en el programa, incluyendo su curso, apoderado titular y año de registro.

Modelos:
- RegistroPie: Representa el registro de un estudiante en el Programa de Integración Escolar.
"""

from django.db import models
from estudiantes.models import Estudiante, ApoderadoTitular, Curso
from datetime import datetime

# Modelo de RegistroPie
class RegistroPie(models.Model):
    """
    Modelo que representa el registro de un estudiante en el Programa de Integración Escolar (PIE).

    Atributos:
    - curso: Curso en el que está inscrito el estudiante.
    - estudiante: Estudiante registrado en el PIE.
    - apoderado_titular: Apoderado titular del estudiante.
    - año_registro: Año en el que se registró al estudiante en el PIE.
    """
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, verbose_name='Curso')
    estudiante = models.OneToOneField(Estudiante, on_delete=models.CASCADE, verbose_name='Estudiante')
    apoderado_titular = models.ForeignKey(ApoderadoTitular, on_delete=models.CASCADE, verbose_name='Apoderado', null=True, blank=True)
    año_registro = models.PositiveIntegerField(verbose_name='Año de Registro en PIE')

    def save(self, *args, **kwargs):
        """
        Sobrescribe el método save para establecer el año de registro al año actual si no se proporciona.
        """
        if self._state.adding and not self.año_registro:
            self.año_registro = datetime.now().year
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.estudiante}'
    
    class Meta:
        verbose_name = 'Pie'
        verbose_name_plural = 'Pies'