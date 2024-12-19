"""
Autores:
- Raúl Córdova Vicencio
- Francisca Olavarría Pavez
- Carlos Olivero Bruno
Fecha: 01 diciembre 2024
"""

from django.utils.decorators import method_decorator
from .funciones import plural_singular

# OBTENER COLOR Y GRUPO DE UN USUARIO (DECORADOR INDEPENDIENTE)

def get_group_and_color(user):
    """
    Obtiene el grupo y el color asociado a un usuario.
    
    Args:
        user (User): El usuario del cual obtener el grupo y color.
    
    Returns:
        tuple: ID del grupo, nombre del grupo, nombre singular del grupo y color asociado.
    """
    group = user.groups.first()

    group_id = None
    group_name = None
    group_name_singular = None
    color = None

    if group:
        # PREGUNTAMOS POR EL GRUPO Y COLOR
        if group.name == 'Funcionarios':
            color = 'bg-zinc-950'
        elif group.name == 'Administradores':
            color = 'bg-gradient-to-tr from-gray-600 to-gray-900'
        elif group.name == 'Coordinadores':
            color = 'bg-gradient-to-tr from-lime-600 to-lime-900'
        elif group.name == 'Coordinadores Suplentes':
            color = 'bg-gradient-to-tr from-gray-600 to-gray-900'
        elif group.name == 'Educadores Diferenciales':
            color = 'bg-gradient-to-tr from-blue-600 to-blue-900'
        elif group.name == 'Psicopedagógos':
            color = 'bg-gradient-to-tr from-purple-600 to-purple-900'
        elif group.name == 'Psicólogos':
            color = 'bg-gradient-to-tr from-indigo-600 to-indigo-900'
        elif group.name == 'Terapeutas Ocupacionales':
            color = 'bg-gradient-to-tr from-red-600 to-red-900'
        elif group.name == 'Fonoaudiologos':
            color = 'bg-gradient-to-tr from-amber-600 to-amber-900'
        elif group.name == 'Técnicos Diferenciales':
            color = 'bg-gradient-to-tr from-pink-600 to-pink-900'
        elif group.name == 'Técnicos Parvularios':
            color = 'bg-gradient-to-tr from-green-600 to-green-900'

        group_id = group.id
        group_name = group.name
        group_name_singular = plural_singular(group.name)

    return group_id, group_name, group_name_singular, color

# DECORADOR INDEPENDIENTE

def add_group_name_to_context(view_class):
    """
    Decorador para agregar el nombre del grupo y el color al contexto de la vista.
    
    Args:
        view_class (View): La clase de la vista a decorar.
    
    Returns:
        View: La clase de la vista decorada.
    """
    original_dispatch = view_class.dispatch

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        group_id, group_name, group_name_singular, color = get_group_and_color(user)

        context = {
            'group_name': group_name,
            'group_name_singular': group_name_singular,
            'color': color
        }
        self.extra_context = context
        return original_dispatch(self, request, *args, **kwargs)

    view_class.dispatch = dispatch
    return view_class