"""
Autores:
- Raúl Córdova Vicencio
- Francisca Olavarría Pavez
- Carlos Olivero Bruno
Fecha: 01 diciembre 2024
"""

import re

# AQUÍ CREAREMOS DIFERENTES FUNCIONES QUE NOS VALIDEN CIERTOS ATRIBUTOS DE LOS MODELOS

# FUNCIÓN PARA PASAR DE PLURAL A SINGULAR LOS GRUPOS
def plural_singular(plural):
    """
    Convierte el nombre de un grupo de plural a singular.
    
    Args:
        plural (str): Nombre del grupo en plural.
    
    Returns:
        str: Nombre del grupo en singular.
    """
    plural_singular = {
        'Funcionarios': 'Funcionario',
        'Administradores': 'Administrador',
        'Coordinadores': 'Coordinador',
        'Coordinadores Suplentes': 'Coordinador Suplente',
        'Educadores Diferenciales': 'Educador Diferencial',
        'Psicopedagógos': 'Psicopedagógo',
        'Psicólogos': 'Psicólogo',
        'Terapeutas Ocupacionales': 'Terapeuta Ocupacional',
        'Fonoaudiologos': 'Fonoaudiologo',
        'Técnicos Diferenciales': 'Técnico Diferencial',
        'Técnicos Parvularios': 'Técnico Parvulario',
    }
    return plural_singular.get(plural, "error")





















