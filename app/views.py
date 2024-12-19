"""
Autores:
- Raúl Córdova Vicencio
- Francisca Olavarría Pavez
- Carlos Olivero Bruno
Fecha: 01 diciembre 2024
"""

import datetime
import re
from typing import Any
from django.http import JsonResponse
from django.utils import timezone # Importamos la zona horaria

from accounts.models import Profile
from estudiantes.models import Curso, Estudiante # Importamos el modelo Profile
from .models import Region, Comuna  # Importa los modelos Region y Comuna
from django.shortcuts import redirect, render # Importamos render y redirect
from django.urls import reverse_lazy, reverse # Importamos reverse_lazy
from django.views import View # Importamos la vista basada en clases
from django.contrib import messages  # Importamos mensajes
from django.views.generic import ListView, TemplateView, CreateView, DetailView # Importamos ListView, TemplateView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.models import Group # Importamos la estructura de los grupos de Django
from .forms import UserForm, ProfileForm, UserCreationForm
from django.contrib.auth.models import User # Importamos el modelo de usuario
from django.contrib.auth import authenticate, login, logout # Importamos la autenticación
from .funciones import plural_singular # Importa la función plural_singular

from .decorators import add_group_name_to_context, get_group_and_color
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin # Importamos la clase UserPassesTestMixin para proteger las vistas URLs
import os # Importamos la librería os
from django.conf import settings    # Importamos la configuración de Django
from django.contrib.auth.views import PasswordChangeView  # Importamos la clase PasswordChangeView
from django.contrib.auth import update_session_auth_hash # Importamos la clase update_session_auth_hash
from django.contrib.auth.views import LoginView # Importamos la clase LoginView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# ____________________________________________________________________________________________________________________________


from django.http import JsonResponse
from .models import Profile  # Asegúrate de importar el modelo correcto

# FUNCIONES PARA VALIDACIONES DE RUT Y FECHA DE NACIMIENTO

# FUNCION PARA VERIFICAR SI EL RUT EXISTE
def verificar_rut(request):
    """
    Verifica si el RUT existe en el sistema.

    Args:
        request (HttpRequest): La solicitud HTTP.

    Returns:
        JsonResponse: Respuesta JSON indicando si el RUT existe.
    """
    rut = request.GET.get('rut', None)
    existe = Profile.objects.filter(rut=rut).exists()
    return JsonResponse({'existe': existe})

# FUNCION PARA VERIFICAR EL DÍGITO VERIFICADOR DEL RUT
def verificar_dv_rut(request):
    """
    Verifica el dígito verificador del RUT.

    Args:
        request (HttpRequest): La solicitud HTTP.

    Returns:
        JsonResponse: Respuesta JSON indicando si el dígito verificador es válido.
    """
    rut = request.GET.get('rut', None)
    if rut:
        rut = rut.replace('.', '').replace('-', '')
        rut_numeros = rut[:-1]
        dv = rut[-1].upper()
        calculado_dv = calcular_dv(rut_numeros)
        es_valido = calculado_dv == dv
        return JsonResponse({'es_valido': es_valido})
    return JsonResponse({'es_valido': False})

# FUNCION PARA CALCULAR EL DÍGITO VERIFICADOR DEL RUT
def calcular_dv(rut_numeros):
    """
    Calcula el dígito verificador del RUT.

    Args:
        rut_numeros (str): Los números del RUT sin el dígito verificador.

    Returns:
        str: El dígito verificador calculado.
    """
    suma = 0
    multiplicador = 2
    for i in reversed(rut_numeros):
        suma += int(i) * multiplicador
        multiplicador += 1
        if multiplicador == 8:
            multiplicador = 2
    resto = suma % 11
    dv = 11 - resto
    if dv == 11:
        return '0'
    elif dv == 10:
        return 'K'
    else:
        return str(dv)
    
# FUNCION PARA VALIDAR LA FECHA DE NACIMIENTO
def validar_fecha_nacimiento(request):
    """
    Valida la fecha de nacimiento.

    Args:
        request (HttpRequest): La solicitud HTTP.

    Returns:
        JsonResponse: Respuesta JSON indicando si la fecha de nacimiento es válida y si la edad está en el rango permitido.
    """
    fecha = request.GET.get('fecha', None)
    if fecha:
        try:
            dia, mes, anio = map(int, fecha.split('-'))
            fecha_nacimiento = datetime.date(anio, mes, dia)
            hoy = datetime.date.today()
            edad = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
            es_valida = 1 <= mes <= 12 and 1 <= dia <= 31 and (mes != 2 or dia <= (29 if anio % 4 == 0 and (anio % 100 != 0 or anio % 400 == 0) else 28))
            edad_valida = 15 <= edad <= 99
            return JsonResponse({'es_valida': es_valida, 'edad_valida': edad_valida})
        except ValueError:
            return JsonResponse({'es_valida': False, 'edad_valida': False})
    return JsonResponse({'es_valida': False, 'edad_valida': False})

#____________________________________________________________________________________________________________________________
#VISTA BASADA EN CLASES PARA LA VIEW DE ERROR
@add_group_name_to_context
class ErrorView(TemplateView):
    """
    Vista para mostrar la página de error.
    """
    template_name = 'error.html'

    #FUNCIÓN PARA MOSTRAR LA IMAGEN DE ERROR
    def get_context_data(self, **kwargs):
        """
        Agrega la imagen de error al contexto.

        Args:
            **kwargs: Argumentos adicionales.

        Returns:
            dict: Contexto actualizado con la imagen de error.
        """
        context = super().get_context_data(**kwargs)
        error_image = os.path.join(settings.MEDIA_ROOT, 'error.png')
        context['error_image'] = error_image
        return context

# ____________________________________________________________________________________________________________________________


# VISTA BASADA EN CLASES DEL INDEX
class IndexView(TemplateView):
    """
    Vista para mostrar la página principal (index).
    """
    template_name = 'index.html'
# ____________________________________________________________________________________________________________________________

# VISTA BASADA EN CLASES DEL HOME

@add_group_name_to_context # Decorador
class HomeView(TemplateView):
    """
    Vista para mostrar la página principal (home).
    """
    template_name = 'home.html'

# ____________________________________________________________________________________________________________________________

# Usamos el decorador `add_group_name_to_context` para agregar el nombre del grupo al contexto de la vista

from .models import AreaAcademica  # Asegúrate de importar el modelo AreaAcademica

@add_group_name_to_context
class ProfileView(TemplateView):
    """
    Vista para mostrar el perfil del usuario.
    """
    template_name = 'profiles/profile.html'
    
    def get_context_data(self, **kwargs):
        """
        Agrega datos adicionales al contexto de la vista del perfil.

        Args:
            **kwargs: Argumentos adicionales.

        Returns:
            dict: Contexto actualizado con datos del perfil.
        """
        context = super().get_context_data(**kwargs)

        # Agregar contexto de cursos con filtro por área académica
        area_id = self.request.GET.get('area')
        if area_id:
            cursos = Curso.objects.filter(area_academica_id=area_id).order_by('area_academica__nombre')
        else:
            cursos = Curso.objects.all().order_by('area_academica__nombre')
        
        cursos_data = []

        for curso in cursos:
            nee_transitorios = Estudiante.objects.filter(cursos=curso, nee='Transitorio').count()
            nee_permanentes = Estudiante.objects.filter(cursos=curso, nee='Permanente').count()
            cursos_data.append({
                'area_academica': curso.area_academica.nombre,
                'curso': curso.nombre,
                'nee_transitorios': nee_transitorios,
                'nee_permanentes': nee_permanentes,
            })

        # Paginación de cursos
        cursos_pages = 10
        paginator = Paginator(cursos_data, cursos_pages)
        number_page = self.request.GET.get('page_cursos')

        try:
            cursos_paginated = paginator.page(number_page)
        except PageNotAnInteger:
            cursos_paginated = paginator.page(1)
        except EmptyPage:
            cursos_paginated = paginator.page(paginator.num_pages)

        context['cursos_data'] = cursos_paginated

        user = self.request.user

        # Obtenemos todos los grupos disponibles, excluyendo los grupos 'Funcionarios' y 'Administradores'
        groups = Group.objects.exclude(name__in=['Administradores', 'Funcionarios'])
        singular_groups = [plural_singular(group.name).capitalize() for group in groups]  # Obtener los nombres singulares de los grupos
        context['groups'] = zip(groups, singular_groups)  # Unimos las 2 variables de grupos para obtener el singular del grupo

        context['user_form'] = UserForm(instance=user)
        context['profile_form'] = ProfileForm(instance=user.profile)
        context['regiones'] = Region.objects.all()
        context['comunas'] = Comuna.objects.all()

        if user.groups.first().name in ['Coordinadores', 'Coordinadores Suplentes']:
            coordinadores_groups = Group.objects.get(name='Coordinadores')
            all_users = User.objects.exclude(groups__in=[coordinadores_groups])
            all_users = all_users.exclude(groups__name='Administradores')
            
            selected_group = self.request.GET.get('group')
            if selected_group:
                all_users = all_users.filter(groups__name=selected_group)

            # Filtrar usuarios activos/desactivados
            show_inactive = self.request.GET.get('show_inactive', 'false') == 'true'
            if show_inactive:
                all_users = all_users.filter(is_active=False)
            else:
                all_users = all_users.filter(is_active=True)

            all_groups = Group.objects.exclude(name__in=['Coordinadores', 'Administradores', 'Funcionarios'])
            user_profiles = []

            for user in all_users:
                profile = user.profile
                user_groups = user.groups.all()
                processed_groups = [plural_singular(group.name) for group in user_groups]

                user_profiles.append({
                    'user': user,
                    'groups': processed_groups,
                    'profile': profile
                })
                
            context['user_profiles'] = user_profiles
            context['all_groups'] = all_groups
            context['show_inactive'] = show_inactive
            
            profiles_pages = 10
            paginator = Paginator(user_profiles, profiles_pages)
            number_page = self.request.GET.get('page')

            try:
                profiles_paginated = paginator.page(number_page)
            except PageNotAnInteger:
                profiles_paginated = paginator.page(1)
            except EmptyPage:
                profiles_paginated = paginator.page(paginator.num_pages)

            context['user_profiles'] = profiles_paginated

        # Agregar contexto de áreas académicas para el filtro
        context['areas_academicas'] = AreaAcademica.objects.all().order_by('nombre')

        return context
    
    def post(self, request, *args, **kwargs):
        """
        Maneja la actualización del perfil del usuario.

        Args:
            request (HttpRequest): La solicitud HTTP.
            *args: Argumentos adicionales.
            **kwargs: Argumentos adicionales.

        Returns:
            HttpResponse: Respuesta HTTP.
        """
        user = self.request.user
        user_form = UserForm(data=request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile_form.save()
            messages.success(request, 'Perfil actualizado exitosamente')
            return redirect('profile')

        context = self.get_context_data()
        context['user_form'] = user_form
        context['profile_form'] = profile_form
        return render(request, 'profiles/profile.html', context)
# ____________________________________________________________________________________________________________________________

#VISTA BASADA EN CLASES PARA CAMBIAR LA CONTRASEÑA DEL USUARIO

@add_group_name_to_context
class ProfilePasswordChangeView(PasswordChangeView):
    """
    Vista para cambiar la contraseña del usuario.
    """
    template_name = 'profiles/change_password.html'
    success_url = reverse_lazy('profile')

    def get_context_data(self, **kwargs):
        """
        Agrega datos adicionales al contexto de la vista de cambio de contraseña.

        Args:
            **kwargs: Argumentos adicionales.

        Returns:
            dict: Contexto actualizado con datos de cambio de contraseña.
        """
        context = super().get_context_data(**kwargs)
        context['password_changed'] = self.request.session.get('password_changed', False)
        return context
    
    def form_valid(self, form):
        """
        Maneja la validación del formulario de cambio de contraseña.

        Args:
            form (Form): El formulario de cambio de contraseña.

        Returns:
            HttpResponse: Respuesta HTTP.
        """
        # Obtener la nueva contraseña
        new_password = form.cleaned_data.get('new_password1')
        
        # Validaciones de complejidad de contraseña
        validation_errors = []
        
        if len(new_password) < 12:
            validation_errors.append('La contraseña debe tener al menos 12 caracteres.')
        
        # Verificar al menos un carácter especial
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', new_password):
            validation_errors.append('La contraseña debe contener al menos un carácter especial.')
        
        # Verificar al menos una mayúscula
        if not re.search(r'[A-Z]', new_password):
            validation_errors.append('La contraseña debe contener al menos una letra mayúscula.')
        
        # Verificar al menos una minúscula
        if not re.search(r'[a-z]', new_password):
            validation_errors.append('La contraseña debe contener al menos una letra minúscula.')
        
        # Verificar al menos un número
        if not re.search(r'[0-9]', new_password):
            validation_errors.append('La contraseña debe contener al menos un número.')

        # Si hay errores de validación, mostrar mensajes de error
        if validation_errors:
            for error in validation_errors:
                messages.error(self.request, error)
            return self.form_invalid(form)

        # Actualizar el campo "creado_por_coordinador" del modelo Profile
        profile = Profile.objects.get(user=self.request.user)
        profile.creado_por_coordinador = False
        profile.save()

        # Usar tags de mensaje específicos
        messages.success(self.request, 'Contraseña cambiada exitosamente')

        # Actualizamos la sesión logeada con la contraseña nueva cambiada
        update_session_auth_hash(self.request, form.user)
        self.request.session['profile_password_changed'] = True
        return super().form_valid(form)
    
    def form_invalid(self, form):
        """
        Maneja la invalidación del formulario de cambio de contraseña.

        Args:
            form (Form): El formulario de cambio de contraseña.

        Returns:
            HttpResponse: Respuesta HTTP.
        """
        # Usar tags de mensaje específicos
        messages.error(self.request, 'Error al cambiar la contraseña')
        return super().form_invalid(form)
# ____________________________________________________________________________________________________________________________

#VISTA PARA RESET DE CONTRASEÑA

class ResetPasswordView(UserPassesTestMixin, LoginRequiredMixin, View):
    """
    Vista para resetear la contraseña de un usuario.
    Solo los administradores y coordinadores pueden resetear contraseñas.
    """
    # Solo los administradores y coordinadores pueden resetear contraseñas
    def test_func(self):
        """
        Verifica si el usuario tiene permisos para resetear contraseñas.

        Returns:
            bool: True si el usuario tiene permisos, False en caso contrario.
        """
        return self.request.user.groups.filter(name__in=['Administradores', 'Coordinadores', 'Coordinadores Suplentes']).exists() 

    def post(self, request, *args, **kwargs):
        """
        Maneja la solicitud de reset de contraseña.

        Args:
            request (HttpRequest): La solicitud HTTP.
            *args: Argumentos adicionales.
            **kwargs: Argumentos adicionales.

        Returns:
            HttpResponse: Respuesta HTTP.
        """
        user_id = kwargs.get('user_id')
        try:
            user = User.objects.get(pk=user_id)
            user.set_password('contraseña')
            user.save()

            # Verificar y establecer is_staff y creado_por_coordinador
            group_id = user.groups.first().id
            if group_id not in [2, 3]:
                user.is_staff = True
                user.save()

            profile = Profile.objects.get(user=user)
            profile.creado_por_coordinador = True
            profile.save()

            messages.success(request, 'Contraseña restablecida exitosamente.')
        except User.DoesNotExist:
            messages.error(request, 'Usuario no encontrado.')
        return redirect('profile_detail', pk=user_id)

# ____________________________________________________________________________________________________________________________

#____________________________________________________________________________________________________________________________
#VISTA PARA DESACTIVAR UN USUARIO

class DesactivarUserView(UserPassesTestMixin, LoginRequiredMixin, View):
    """
    Vista para desactivar un usuario.
    Solo los administradores y coordinadores pueden desactivar usuarios.
    """
    def test_func(self):
        """
        Verifica si el usuario tiene permisos para desactivar usuarios.

        Returns:
            bool: True si el usuario tiene permisos, False en caso contrario.
        """
        return self.request.user.groups.filter(name__in=['Administradores', 'Coordinadores', 'Coordinadores Suplentes']).exists()

    def post(self, request, *args, **kwargs):
        """
        Maneja la solicitud de desactivación de usuario.

        Args:
            request (HttpRequest): La solicitud HTTP.
            *args: Argumentos adicionales.
            **kwargs: Argumentos adicionales.

        Returns:
            HttpResponse: Respuesta HTTP.
        """
        user_id = kwargs.get('user_id')
        try:
            user = User.objects.get(pk=user_id)
            user.is_active = False
            user.save()
            messages.success(request, 'Usuario desactivado exitosamente.')
        except User.DoesNotExist:
            messages.error(request, 'Usuario no encontrado.')
        return redirect('profile')
    

# ____________________________________________________________________________________________________________________________
# VISTA PARA ACTIVAR UN USUARIO

class ActivarUserView(UserPassesTestMixin, LoginRequiredMixin, View):
    """
    Vista para activar un usuario.
    Solo los administradores y coordinadores pueden activar usuarios.
    """
    def test_func(self):
        """
        Verifica si el usuario tiene permisos para activar usuarios.

        Returns:
            bool: True si el usuario tiene permisos, False en caso contrario.
        """
        return self.request.user.groups.filter(name__in=['Administradores', 'Coordinadores', 'Coordinadores Suplentes']).exists()

    def post(self, request, *args, **kwargs):
        """
        Maneja la solicitud de activación de usuario.

        Args:
            request (HttpRequest): La solicitud HTTP.
            *args: Argumentos adicionales.
            **kwargs: Argumentos adicionales.

        Returns:
            HttpResponse: Respuesta HTTP.
        """
        user_id = kwargs.get('user_id')
        try:
            user = User.objects.get(pk=user_id)
            user.is_active = True
            user.save()
            messages.success(request, 'Usuario activado exitosamente.')
        except User.DoesNotExist:
            messages.error(request, 'Usuario no encontrado.')
        return redirect('profile')
#____________________________________________________________________________________________________________________________
#CREAMOS UN NUEVO USUARIO DESDE EL ROL DE UN COORDINADOR O ADMINISTRADOR

#VISTA BASADA EN CLASES DE REGISTRO DE USUARIOS (COORDINADORES Y ADMINISTRADORES)
@add_group_name_to_context
class AddUserView(UserPassesTestMixin, LoginRequiredMixin, CreateView):
    """
    Vista para registrar un nuevo usuario desde el rol de un coordinador o administrador.
    """
    model = User
    form_class = UserCreationForm
    template_name = 'profiles/add_user.html'
    success_url = '/profile/'

    def test_func(self):
        """
        Verifica si el usuario tiene permisos para registrar nuevos usuarios.

        Returns:
            bool: True si el usuario tiene permisos, False en caso contrario.
        """
        return self.request.user.groups.first().name in ['Coordinadores', 'Administradores', 'Coordinadores Suplentes']

    def handle_no_permission(self):
        """
        Maneja la falta de permisos para registrar nuevos usuarios.

        Returns:
            HttpResponse: Respuesta HTTP redirigiendo a la página de error.
        """
        return redirect('error')

    def get_context_data(self, **kwargs):
        """
        Agrega datos adicionales al contexto de la vista de registro de usuario.

        Args:
            **kwargs: Argumentos adicionales.

        Returns:
            dict: Contexto actualizado con datos de registro de usuario.
        """
        context = super().get_context_data(**kwargs)
        groups = Group.objects.exclude(name__in=['Administradores', 'Funcionarios', 'Coordinadores'])
        singular_groups = [group.name.capitalize() for group in groups]
        context['groups'] = zip(groups, singular_groups)
        return context

    def form_valid(self, form):
        """
        Maneja la validación del formulario de registro de usuario.

        Args:
            form (Form): El formulario de registro de usuario.

        Returns:
            HttpResponse: Respuesta HTTP.
        """
        group_id = self.request.POST['group']
        group = Group.objects.get(id=group_id)
        user = form.save(commit=False)
        user.set_password('contraseña')
        if group_id not in ['2', '3']:
            user.is_staff = True
        user.save()

        # Actualizar o crear perfil con apellidos y rut
        profile, created = Profile.objects.get_or_create(user=user)
        profile.apellido_paterno = form.cleaned_data.get('apellido_paterno').capitalize()
        profile.apellido_materno = form.cleaned_data.get('apellido_materno').capitalize()
        profile.rut = form.cleaned_data.get('rut')
        profile.save()

        user.groups.clear()
        user.groups.add(group)
        messages.success(self.request, 'Usuario creado exitosamente')
        return super().form_valid(form)

    def form_invalid(self, form):
        """
        Maneja la invalidación del formulario de registro de usuario.

        Args:
            form (Form): El formulario de registro de usuario.

        Returns:
            HttpResponse: Respuesta HTTP.
        """
        return self.render_to_response(self.get_context_data(form=form))
    # ____________________________________________________________________________________________________________________________

#VISTA BASADA EN CLASES PARA LA VIEW DE LOGIN PERSONALIZADO
#Este login evaluara si es nuevo usuario y si es asi lo va a redireccionar a cambiar la contraseña
from django.contrib.messages import constants as message_constants

from django.contrib.auth import authenticate, get_user_model

class CustomLoginView(LoginView):
    """
    Vista para el login personalizado.
    """
    def form_valid(self, form):
        """
        Maneja la validación del formulario de login.

        Args:
            form (Form): El formulario de login.

        Returns:
            HttpResponse: Respuesta HTTP.
        """
        print("Formulario válido: Usuario autenticado correctamente.")
        messages.success(self.request, 'Bienvenido!')
        response = super().form_valid(form)

        # Accedemos al perfil de usuario
        profile = self.request.user.profile

        # Verificamos el valor del campo "creado por el coordinador del modelo Profile"
        if profile.creado_por_coordinador:
            messages.warning(self.request, 'Bienvenido, debe cambiar su contraseña ahora!')
            response['Location'] = reverse_lazy('profile_password_change')
            response.status_code = 302

        return response

    def form_invalid(self, form):
        """
        Maneja la invalidación del formulario de login.

        Args:
            form (Form): El formulario de login.

        Returns:
            HttpResponse: Respuesta HTTP.
        """
        # Verificamos si el usuario ha sido deshabilitado
        username = form.cleaned_data.get('username')
        User = get_user_model()
        try:
            user = User.objects.get(username=username)
            if not user.is_active:
                messages.error(self.request, 'Usuario Deshabilitado, contacte al Coordinador del PIE.')
                return super().form_invalid(form)
        except User.DoesNotExist:
            pass

        print("Formulario inválido: Nombre de usuario o contraseña incorrectos.")
        messages.error(self.request, 'Nombre de usuario o contraseña incorrectos.')
        return super().form_invalid(form)

    def get_success_url(self):
        """
        Retorna la URL de éxito después del login.

        Returns:
            str: La URL de éxito.
        """
        return super().get_success_url()

# ____________________________________________________________________________________________________________________________

#VISTA BASADA EN CLASES PARA LA VIEW DE PERFIL DETALLADO DE UN USUARIO

@add_group_name_to_context
class UserDetailView(LoginRequiredMixin, DetailView):
    """
    Vista para mostrar el perfil detallado de un usuario.
    """
    model = User
    template_name = 'profiles/profile_detail.html'
    context_object_name = 'user_profile'

    def get_context_data(self, **kwargs):
        """
        Agrega datos adicionales al contexto de la vista de perfil detallado.

        Args:
            **kwargs: Argumentos adicionales.

        Returns:
            dict: Contexto actualizado con datos de perfil detallado.
        """
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        current_user = self.request.user
        group_id, group_name, group_name_singular, color = get_group_and_color(user)
        


        # Obtenemos todos los grupos disponibles, excluyendo los grupos 'Funcionarios' y 'Administradores'
        groups = Group.objects.exclude(name__in=['Coordinadores', 'Administradores', 'Funcionarios'])
        singular_groups = [plural_singular(group.name).capitalize() for group in groups]
        context['groups'] = zip(groups, singular_groups)

        context['regiones'] = Region.objects.all()
        context['comunas'] = Comuna.objects.all()
        context['group_id_user'] = group_id
        context['group_name_user'] = group_name
        context['group_name_singular_user'] = group_name_singular
        context['color_user'] = color

        # Verificar si el usuario actual es un "Coordinador Suplente"
        context['is_coordinador_suplente'] = current_user.groups.filter(name='Coordinadores Suplentes').exists()

        return context

# Editamos un usuario según su pk
def superuser_edit(request, user_id):
    user = User.objects.get(pk=user_id)
    current_user = request.user

    # Verificamos si es Super Usuario o "Coordinador Suplente"
    if not current_user.is_superuser and not current_user.groups.filter(name='Coordinadores Suplentes').exists():
        return redirect('error')

    # Verificamos los datos que ingresamos en el formulario
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=user.profile)
        group = request.POST.get('group')

        # Validación del formulario
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            # Evitar que los "Coordinadores Suplentes" cambien su propio grupo
            if current_user != user or current_user.is_superuser:
                user.groups.clear()
                user.groups.add(group)

            messages.success(request, 'Usuario editado exitosamente')
            return redirect('profile_detail', pk=user.pk)

    else:
        user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'is_coordinador_suplente': current_user.groups.filter(name='Coordinadores Suplentes').exists()
    }
    return render(request, 'profiles/profile_detail.html', context)
        
# ___________________________________________________________________________________________________________________________