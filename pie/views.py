"""
Autores:
Raúl Córdova Vicencio
Francisca Olavarría Pavez
Carlos Olivero Bruno

Fecha: 01 diciembre 2024

Descripción:
Este módulo define las vistas para la gestión del Programa de Integración Escolar (PIE). Incluye vistas para listar, crear y actualizar registros de PIE, proporcionando una interfaz de usuario para interactuar con los datos de los estudiantes y sus apoderados.

Vistas:
- ListPieView: Vista basada en clase para listar los registros de PIE.
- AddRegistroPieView: Vista basada en clase para agregar un nuevo registro de PIE.
"""

from datetime import datetime
from typing import Any
from django.http.response import HttpResponseRedirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from app.decorators import add_group_name_to_context
from localidad.models import Region, Comuna
from estudiantes.models import AreaAcademica, Curso, Estudiante, ApoderadoTitular
from .models import RegistroPie
from .forms import AddRegistroPieForm
from django.shortcuts import redirect, render # Importamos render y redirect
from django.urls import reverse_lazy, reverse # Importamos reverse_lazy
from django.views import View # Importamos la vista basada en clases
from django.contrib import messages  # Importamos mensajes
from django.views.generic import ListView, TemplateView, CreateView, UpdateView, DeleteView, DetailView # Importamos ListView, TemplateView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.models import Group # Importamos la estructura de los grupos de Django
from django.contrib.auth.models import User # Importamos el modelo de usuario
from django.contrib.auth import authenticate, login, logout # Importamos la autenticación
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin # Importamos la clase UserPassesTestMixin para proteger las vistas URLs
import os # Importamos la librería os
from django.conf import settings    # Importamos la configuración de Django
from django.contrib.auth.views import PasswordChangeView  # Importamos la clase PasswordChangeView
from django.contrib.auth import update_session_auth_hash # Importamos la clase update_session_auth_hash
from django.contrib.auth.views import LoginView # Importamos la clase LoginView
# ____________________________________________________________________________________
# Create your views here.
# VISTA BASADA EN CLASES PARA LISTAR REGISTRO DEL PIE
# VISTA BASADA EN CLASES PARA LISTAR REGISTRO DEL PIE
@add_group_name_to_context
class ListPieView(ListView):
    """
    Vista basada en clase para listar los registros de PIE.

    Atributos:
    - model: Modelo a utilizar (RegistroPie).
    - template_name: Nombre de la plantilla a utilizar.
    - context_object_name: Nombre del objeto de contexto.
    - paginate_by: Número de elementos por página.
    """
    model = RegistroPie
    template_name = 'pie/pie.html'
    context_object_name = 'pies'  # Nombre del objeto de contexto
    paginate_by = 10  # Número de elementos por página

    def get_queryset(self):
        """
        Obtiene el conjunto de registros de PIE, filtrando por área académica y año si se proporcionan.

        Retorna:
        - queryset: Conjunto de registros filtrados.
        """
        queryset = super().get_queryset()
        area_filtro = self.request.GET.get('area_filtro')
        año_filtro = self.request.GET.get('año_filtro', datetime.now().year)
        if area_filtro:
            queryset = queryset.filter(estudiante__cursos__area_academica_id=area_filtro)
        if año_filtro:
            queryset = queryset.filter(año_registro=año_filtro)
        return queryset

    def get_context_data(self, **kwargs):
        """
        Obtiene el contexto de la vista, incluyendo los filtros y la paginación.

        Retorna:
        - context: Contexto de la vista.
        """
        context = super().get_context_data(**kwargs)
        
        # Obtener los filtros desde la solicitud GET
        area_filtro = self.request.GET.get('area_filtro')
        año_filtro = self.request.GET.get('año_filtro', datetime.now().year)
        
        # Filtrar los registros de PIE según el área académica y año seleccionados
        if area_filtro:
            pies_list = RegistroPie.objects.filter(estudiante__cursos__area_academica_id=area_filtro, año_registro=año_filtro)
        else:
            pies_list = RegistroPie.objects.filter(año_registro=año_filtro)
        
        # Paginación
        paginator = Paginator(pies_list, self.paginate_by)
        number_page = self.request.GET.get('page')
        
        try:
            pies_paginated = paginator.page(number_page)
        except PageNotAnInteger:
            pies_paginated = paginator.page(1)
        except EmptyPage:
            pies_paginated = paginator.page(paginator.num_pages)
        
        context['pies'] = pies_paginated
        
        # Agregar las opciones de área académica y año al contexto
        context['areas_academicas'] = AreaAcademica.objects.all()
        context['opciones_nee'] = Estudiante._meta.get_field('nee').choices
        context['opciones_curso'] = Curso.objects.all()
        context['opciones_etnia'] = Estudiante._meta.get_field('etnia').choices
        context['regiones'] = Region.objects.all()
        context['comunas'] = Comuna.objects.all()
        context['area_filtro'] = area_filtro
        context['año_filtro'] = año_filtro
        context['años_matricula'] = RegistroPie.objects.values_list('año_registro', flat=True).distinct()
        
        return context

#_________________________________________________________________________________________________________________

#VISTA BASADA EN CLASES PARA AGREGAR REGISTRO DEL PIE

@add_group_name_to_context
class AddRegistroPieView(UserPassesTestMixin, LoginRequiredMixin, CreateView):
    """
    Vista basada en clase para agregar un nuevo registro de PIE.

    Atributos:
    - model: Modelo a utilizar (RegistroPie).
    - template_name: Nombre de la plantilla a utilizar.
    - form_class: Clase del formulario a utilizar.
    - success_url: URL de redirección después de un registro exitoso.
    """
    model = RegistroPie
    template_name = 'pie/pie_detail.html'
    form_class = AddRegistroPieForm  # Aquí debe ser la clase del formulario, no una cadena de texto
    success_url = reverse_lazy('pie')

    #Creamos una función para que solo el coordinador y el administrador puedan registrar usuarios
    def test_func(self):
        """
        Verifica si el usuario actual pertenece al grupo 'Coordinadores' o 'Administradores'.

        Retorna:
        - Booleano indicando si el usuario tiene permiso.
        """
        return self.request.user.groups.first().name == 'Coordinadores' or self.request.user.groups.first().name == 'Administradores'
    
    #Función si el usuario no tiene permiso
    def handle_no_permission(self):
        """
        Redirige a una página de error si el usuario no tiene permiso.
        """
        return redirect('error')
    
     #Recuperamos los objetos del modelo PIE
    def get_context_data(self, **kwargs):
        """
        Obtiene el contexto de la vista, incluyendo los registros de PIE.

        Retorna:
        - context: Contexto de la vista.
        """
        context = super().get_context_data(**kwargs) #Obtenemos el contexto

        context['pies'] = RegistroPie.objects.all()

        return context





