"""
Autores:
Raúl Córdova Vicencio
Francisca Olavarría Pavez
Carlos Olivero Bruno

Fecha: 01 diciembre 2024

Descripción:
Este módulo define las vistas para la aplicación de gestión de estudiantes. Incluye vistas para listar, crear, actualizar y detallar información sobre cursos, estudiantes, apoderados, bitácoras y formularios de evaluación. Cada vista está diseñada para interactuar con los modelos y formularios correspondientes, proporcionando una interfaz de usuario coherente y funcional.

Vistas:
- CursosListView: Vista basada en clase para listar los cursos.
- AddEstudianteView: Vista basada en clase para agregar un nuevo estudiante.
- EstudianteUpdateView: Vista basada en clase para actualizar la información de un estudiante.
- EstudianteDetailView: Vista basada en clase para ver el detalle de un estudiante y sus apoderados.
- ApoderadoTitularDetailView: Vista basada en clase para ver el detalle de un apoderado titular.
- ApoderadoTitularUpdateView: Vista basada en clase para actualizar la información de un apoderado titular.
- AddBitacoraEstudianteView: Vista basada en clase para agregar una bitácora de estudiante.
- BitacoraEstudianteListView: Vista basada en clase para listar las bitácoras de un estudiante.
- BitacoraEstudianteDetailView: Vista basada en clase para ver el detalle de una bitácora de estudiante.
- BitacoraEstudianteUpdateView: Vista basada en clase para actualizar una bitácora de estudiante.
- BitacoraRedirectView: Vista basada en clase para redirigir a una bitácora específica.
- PromediosEstudianteView: Vista basada en clase para ver los promedios de un estudiante.
- AnamnesisEstudianteUpdateView: Vista basada en clase para actualizar la anamnesis de un estudiante.
- PaiEstudianteUpdateView: Vista basada en clase para actualizar el PAI de un estudiante.
- PaciEstudianteUpdateView: Vista basada en clase para actualizar el PACI de un estudiante.

Decoradores:
- add_group_name_to_context: Decorador para agregar el nombre del grupo al contexto.

Funciones:
- plural_singular: Función personalizada para manejar el plural y singular de los nombres de grupo.
"""

# Importaciones de Django core
import base64  # Para codificación y decodificación de datos en base64
import io  # Para manejar flujos de entrada y salida
from django.conf import settings  # Para acceder a la configuración de Django
from babel.dates import format_date  # Para formatear fechas
from django.contrib import messages  # Para manejar mensajes de usuario
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash  # Para autenticación y manejo de sesiones de usuario
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin  # Para restricciones de acceso basadas en permisos y autenticación
from django.contrib.auth.models import Group  # Para manejar grupos de usuarios
from django.contrib.auth.views import PasswordChangeView  # Para vistas de cambio de contraseña
from django.core.serializers.json import DjangoJSONEncoder  # Para serialization JSON
from django.http import HttpResponse, JsonResponse  # Para manejar respuestas HTTP y JSON
from django.shortcuts import get_object_or_404, redirect, render  # Para atajos de vistas
from django.template.loader import render_to_string  # Para renderizar plantillas a cadenas
from django.templatetags.static import static  # Para manejar archivos estáticos
from django.urls import reverse_lazy, reverse  # Para manejo de URLs
from django.utils import timezone  # Para manejo de zonas horarias
from django.views import View  # Para vistas basadas en clases
from django.views.generic import (  # Para vistas genéricas basadas en clases
    ListView, 
    TemplateView, 
    CreateView, 
    UpdateView, 
    DeleteView, 
    DetailView
)
from django.views.generic.edit import UpdateView
from django.db import transaction  # Para manejo de transacciones

# Importaciones de terceros
from weasyprint import HTML  # Para generar PDFs a partir de HTML

# Importaciones del proyecto
from accounts.models import Profile  # Modelo de perfil de usuario
from app.decorators import add_group_name_to_context  # Decorador para agregar el nombre del grupo al contexto
from app.funciones import plural_singular  # Función personalizada para manejo de plural y singular
from app.models import Asignatura, BitacoraEstudiante  # Modelos personalizados
from localidad.models import Region, Comuna  # Modelos de localidad
from pie.models import RegistroPie  # Modelo de registro PIE
from .forms import (  # Formularios personalizados
    EstudianteForm, 
    ApoderadoTitularForm, 
    BitacoraEstudianteForm,
    PromedioMensualHistoricoForm,
    PromedioSemanalHistoricoForm,
    AnamnesisEstudianteForm,
    FamiliarFormSet,
    PaiEstudianteForm, 
    EquipoResponsablePaiFormSet, 
    DocentesFormSet, 
    FamiliaFormSet, 
    EstrategiasDiversificadasFormSet, 
    ApoyosEspecializadosFormSet, 
    HorarioApoyosFormSet, 
    FirmaFormSet,
    PaciForm, 
    EquipoResponsablePaciFormSet, 
    AulaRecursosFormSet, 
    AulaRegularFormSet, 
    PresentacionRepresentacionFormSet, 
    MediosEjecucionExpresionFormSet, 
    MultiplesMediosFormSet, 
    EntornoFormSet, 
    OrganizacionTiempoFormSet, 
    GraduacionComplejidadFormSet, 
    PriorizacionOAFormSet, 
    TemporalizacionFormSet, 
    EnriquecimientoCurriculumFormSet, 
    ObjetivosAprendizajeFormSet, 
    ColumnasObjetivosAprendizajeFormSet,
    ColaboracionFamiliaFormSet, 
    CritEvaluacionPromocionFormSet, 
    SeguimientoPaciFormSet, 
    FirmaPaciFormSet
)
from .models import (  # Modelos personalizados
    Estudiante, 
    ApoderadoTitular, 
    AreaAcademica,
    Curso,
    Paci,
    Pai,
    PromedioDia,
    PromedioSemanalHistorico,
    PromedioMensualHistorico,
    AnamnesisEstudiante,
    Familiar,
    EquipoResponsablePai, 
    Docentes, 
    Familia, 
    EstrategiasDiversificadas, 
    ApoyosEspecializados, 
    HorarioApoyos, 
    Firma,
    Region,
    Comuna,
    Profile
)

# Importaciones de Python estándar
import json  # Para manejo de datos JSON
import os  # Para manejo de operaciones del sistema operativo
from datetime import datetime  # Para manejo de fechas y horas

# ____________________________________________________________________________________

# Create your views here.

class CursosListView(ListView):
    model = Curso
    template_name = 'pie/cursos_list.html'
    context_object_name = 'cursos_data'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cursos = Curso.objects.all().order_by('area_academica__nombre', 'nombre')
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

        context['cursos_data'] = cursos_data
        return context

# VISTA BASADA EN CLASES PARA AGREGAR UN ESTUDIANTE# VISTA BASADA EN CLASES PARA AGREGAR UN ESTUDIANTE

@add_group_name_to_context
class AddEstudianteView(UserPassesTestMixin, LoginRequiredMixin, CreateView):
    model = Estudiante  # Modelo que se utilizará para crear al estudiante.
    template_name = 'pie/add_estudiante.html'  # Template que se utilizará para mostrar el formulario de registro del estudiante.
    form_class = EstudianteForm  # Especificamos la clase de formulario que se utilizará para el estudiante.
    success_url = reverse_lazy('pie')  # Especificamos la URL a la que se redirigirá después de un registro exitoso.

    def test_func(self):
        return self.request.user.groups.exists()
    # Función que se ejecuta cuando un usuario no tiene permiso para acceder a esta vista y lo redirige a una página de error.

    def handle_no_permission(self):
        return redirect('error')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['opciones_nee'] = Estudiante._meta.get_field('nee').choices
        context['opciones_etnia'] = Estudiante._meta.get_field('etnia').choices
        context['opciones_curso'] = Curso.objects.all()
        context['regiones'] = Region.objects.all()
        context['comunas'] = Comuna.objects.all()
        context['areas_academicas'] = AreaAcademica.objects.all()
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Estudiante agregado exitosamente')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Por favor, corrija los errores en el formulario.')
        return super().form_invalid(form)

#____________________________________________________________________________________________________________________

# VISTA BASADA EN CLASES PARA EDITAR A UN ESTUDIANTE
@add_group_name_to_context
class EstudianteUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Estudiante
    template_name = 'pie/estudiante_edit.html'
    form_class = EstudianteForm
    success_url = reverse_lazy('estudiante')

    def test_func(self):
        return self.request.user.groups.exists()
    
    def handle_no_permission(self):
        return redirect('error')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['estudiante'] = self.object
        context['opciones_nee'] = Estudiante._meta.get_field('nee').choices
        context['opciones_etnia'] = Estudiante._meta.get_field('etnia').choices
        context['opciones_curso'] = Curso.objects.all()
        context['regiones'] = Region.objects.all()
        context['comunas'] = Comuna.objects.all()
        context['areas_academicas'] = AreaAcademica.objects.all()
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Estudiante actualizado exitosamente.')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Por favor, corrija los errores en el formulario.')
        return super().form_invalid(form)
    
    def get_success_url(self):
        return reverse('estudiante', kwargs={'pk': self.object.pk})
# ____________________________________________________________________________________


# VISTA BASADA EN CLASES PARA VER EL DETALLE DE UN ESTUDIANTE Y LOS APODERADOS# VISTA BASADA EN CLASES PARA VER EL DETALLE DE UN ESTUDIANTE Y LOS APODERADOS
@add_group_name_to_context
class EstudianteDetailView(LoginRequiredMixin, DetailView):
    model = Estudiante
    template_name = 'pie/estudiante.html'
    context_object_name = 'estudiante'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obtenemos el Estudiante
        estudiante = self.get_object()

        # Obtener el apoderado titular del estudiante
        apoderado_titular = estudiante.apoderadotitular

        # Obtener los informes de Anamnesis, PAI y PACI del estudiante
        anamnesis = AnamnesisEstudiante.objects.filter(estudiante=estudiante).first()
        pai = Pai.objects.filter(estudiante=estudiante).first()
        paci = Paci.objects.filter(estudiante=estudiante).first()

        # Agregar los apoderados y los informes al contexto
        context['apoderado_titular'] = apoderado_titular
        context['anamnesis'] = anamnesis
        context['pai'] = pai
        context['paci'] = paci

        # Obtener el nombre del grupo en singular
        if anamnesis and anamnesis.entrevistador:
            group_name = anamnesis.entrevistador.user.groups.first().name
            context['group_name_singular_anamnesis'] = plural_singular(group_name)
        if pai and pai.coordinador_pie:
            group_name = pai.coordinador_pie.user.groups.first().name
            context['group_name_singular_pai'] = plural_singular(group_name)
        if paci and paci.coordinador_pie:
            group_name = paci.coordinador_pie.user.groups.first().name
            context['group_name_singular_paci'] = plural_singular(group_name)

        # Datos básicos
        context.update({
            'regiones': Region.objects.all(),
            'comunas': Comuna.objects.all(),
            'estudiantes': Estudiante.objects.all(),
            'estudiante': estudiante,
            'anamnesis_estudiante': anamnesis,
            'usuario_logueado': self.request.user,
        })

        # Opciones de los campos de selección
        context.update({
            'opciones_pais': AnamnesisEstudiante._meta.get_field('pais_natal').choices,
            'opciones_lengua': AnamnesisEstudiante._meta.get_field('lengua').choices,
            'opciones_sexo': AnamnesisEstudiante._meta.get_field('sexo').choices,
            'opciones_parentesco': Familiar._meta.get_field('parentesco').choices,
        })

        # Campos booleanos del modelo
        campos_booleanos = [
            'pediatria', 'kinesiologia', 'genetico', 'fonoaudiologia',
            'neurologia', 'psicologia', 'psiquiatria', 'psicopedagogia',
            'terapia_ocupacional', 'otro', 'perdida_auditiva',
            'perdida_visual', 'motor', 'paraplejia', 'trastorno_conductual'
        ]
        for campo in campos_booleanos:
            context[campo] = getattr(anamnesis, campo) if anamnesis else None

        context['otros'] = anamnesis.otros if anamnesis else None
        context['alumno_trabajador'] = anamnesis.alumno_trabajador if anamnesis else None

        # Convertir nombre del grupo a singular
        if self.request.user.groups.exists():
            grupo_plural = self.request.user.groups.first().name
            grupo_singular = plural_singular(grupo_plural)
            context['cargo'] = grupo_singular

        # Manejo del formset de familiares
        if self.request.POST:
            context['familiar_formset'] = FamiliarFormSet(
                self.request.POST,
                instance=anamnesis
            )
        else:
            context['familiar_formset'] = FamiliarFormSet(
                instance=anamnesis
            )

        context['opciones_nee'] = Estudiante._meta.get_field('nee').choices
        context['opciones_curso'] = Curso.objects.all()
        context['opciones_etnia'] = Estudiante._meta.get_field('etnia').choices
        context['opciones_salud'] = ApoderadoTitular._meta.get_field('salud').choices
        context['areas_academicas'] = AreaAcademica.objects.all()
        context['logo_liceo_url'] = self.request.build_absolute_uri(static('Imagenes/LOGO LICEO TECNICO ADULTOS.jpg'))
        context['logo_servicio_url'] = self.request.build_absolute_uri(static('Imagenes/Servicio_local.jpg'))
        context['logo_pie_url'] = self.request.build_absolute_uri(static('Imagenes/Imagen_PIE.jpg'))

        # Agregar contexto adicional de Pai
        if pai:
            context.update({
                'equipo_responsable': pai.equipo_responsable.all(),
                'docentes': pai.docentes.all(),
                'familia': pai.familia.all(),
                'estrategias_diversificadas': pai.estrategias_diversificadas.all(),
                'apoyos_especializados': pai.apoyos_especializados.all(),
                'horario_apoyos': pai.horario_apoyos.all(),
                'firma_equipo': pai.firma.all(),
            })

        # Agregar contexto adicional de Paci
        if paci:
            context.update({
                'equipo_responsable_paci': paci.equipo_responsable.all(),
                'aula_recursos': paci.aula_recursos.all(),
                'aula_regular': paci.aula_regular.all(),
                'presentacion_representacion': paci.presentacion_representacion.all(),
                'medios_ejecucion_expresion': paci.medios_ejecucion_expresion.all(),
                'multiples_medios': paci.multiples_medios.all(),
                'entorno': paci.entorno.all(),
                'organizacion_tiempo': paci.organizacion_tiempo.all(),
                'graduacion_complejidad': paci.graduacion_complejidad.all(),
                'priorizacion_oa': paci.priorizacion_oa.all(),
                'temporalizacion': paci.temporalizacion.all(),
                'enriquecimiento_curriculum': paci.enriquecimiento_curriculum.all(),
                'objetivos_aprendizaje': paci.objetivos_aprendizaje.all(),
                'columnas_objetivos_aprendizaje': paci.columnas_objetivos_aprendizaje.all(),
                'colaboracion_familia': paci.colaboracion_familia.all(),
                'crit_evaluacion_promocion': paci.crit_evaluacion_promocion.all(),
                'seguimiento_paci': paci.seguimiento_paci.all(),
                'firma_paci': paci.firma_paci.all(),
            })

        return context
#____________________________________________________________________________________________________________________

# VISTA BASADA EN CLASES PARA DETALLE DE UN APODERADO TITULAR
@add_group_name_to_context
class ApoderadoTitularDetailView(LoginRequiredMixin, DetailView):
    model = ApoderadoTitular
    template_name = 'pie/apoderado_titular_edit.html'
    context_object_name = 'apoderado_titular'

# VISTA BASADA EN CLASES PARA EDITAR UN APODERADO TITULAR
@add_group_name_to_context
class ApoderadoTitularUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = ApoderadoTitular
    template_name = 'pie/apoderado_titular_edit.html'
    form_class = ApoderadoTitularForm
    success_url = reverse_lazy('estudiante')  # Lo ajustaremos más abajo

    def test_func(self):
        return self.request.user.groups.exists()

    def handle_no_permission(self):
        return redirect('error')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['apoderado_titular'] = self.object
        context['opciones_etnia'] = ApoderadoTitular._meta.get_field('etnia').choices
        context['opciones_salud'] = ApoderadoTitular._meta.get_field('salud').choices
        context['regiones'] = Region.objects.all()
        context['comunas'] = Comuna.objects.all()
        context['estudiantes'] = Estudiante.objects.all()
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        try:
            registro_pie = RegistroPie.objects.get(estudiante=self.object.estudiante)
            registro_pie.apoderado_titular = self.object
            registro_pie.save()
        except RegistroPie.DoesNotExist:
            pass
        messages.success(self.request, 'Apoderado Titular actualizado exitosamente.')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Por favor, corrija los errores en el formulario.')
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('estudiante', kwargs={'pk': self.object.estudiante.pk})

# -------------------------------------------------------------------------------------------------------------------
# VISTA BASADA EN CLASES PARA DETALLE DE UN APODERADO TITULAR
@add_group_name_to_context
class ApoderadoTitularDetailView(LoginRequiredMixin, DetailView):
    model = ApoderadoTitular
    template_name = 'pie/apoderado_titular_edit.html'
    context_object_name = 'apoderado_titular'
# -------------------------------------------------------------------------------------------------------------------

# VISTA BASADA EN CLASES PARA EDITAR UN APODERADO TITULAR
@add_group_name_to_context
class ApoderadoTitularUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = ApoderadoTitular
    template_name = 'pie/apoderado_titular_edit.html'
    form_class = ApoderadoTitularForm
    success_url = reverse_lazy('estudiante')  # Lo ajustaremos más abajo

    # Verifica si el usuario actual tiene permiso para acceder a esta vista
    def test_func(self):
        return self.request.user.groups.exists()

    # Redirige a una página de error si el usuario no tiene permisos
    def handle_no_permission(self):
        return redirect('error')

    # Añadir datos adicionales al contexto, como opciones de etnia y salud, regiones y comunas
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['apoderado_titular'] = self.object
        context['opciones_etnia'] = ApoderadoTitular._meta.get_field('etnia').choices
        context['opciones_salud'] = ApoderadoTitular._meta.get_field('salud').choices
        context['regiones'] = Region.objects.all()
        context['comunas'] = Comuna.objects.all()
        context['estudiantes'] = Estudiante.objects.all()
        return context

    # Actualiza también el apoderado titular en el RegistroPie correspondiente cuando el formulario es válido
    def form_valid(self, form):
        # Guardar los cambios en el ApoderadoTitular
        response = super().form_valid(form)
        
        # Buscar y actualizar el RegistroPie correspondiente al estudiante
        try:
            registro_pie = RegistroPie.objects.get(estudiante=self.object.estudiante)
            registro_pie.apoderado_titular = self.object  # Asigna el apoderado titular actualizado
            registro_pie.save()  # Guarda los cambios en RegistroPie
        except RegistroPie.DoesNotExist:
            pass  # Si no existe un registro PIE, no hace nada
        
        # Mensaje de éxito
        messages.success(self.request, 'Apoderado Titular actualizado exitosamente.')
        return response

    # Manejar el caso de un formulario inválido
    def form_invalid(self, form):
        messages.error(self.request, 'Por favor, corrija los errores en el formulario.')
        return super().form_invalid(form)

    # Redirigir al detalle del estudiante tras una actualización exitosa
    def get_success_url(self):
        return reverse('estudiante', kwargs={'pk': self.object.estudiante.pk})  # Redirige al detalle del estudiante


# -------------------------------------------------------------------------------------------------------------------

#VISTA BASA EN CLASES PARA BITÁCORAS
# VISTA BASADA EN CLASES PARA REGISTRAR UNA BITACORA
# 
# views.py
@add_group_name_to_context
class AddBitacoraEstudianteView(UserPassesTestMixin, LoginRequiredMixin, CreateView):
    model = BitacoraEstudiante
    form_class = BitacoraEstudianteForm
    template_name = 'informes/add_bitacora_estudiante.html'

    def test_func(self):
        return self.request.user.groups.exists()

    def handle_no_permission(self):
        return redirect('error')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        groups = Group.objects.all()
        singular_groups = [plural_singular(group.name).capitalize() for group in groups]
        context['groups'] = zip(groups, singular_groups)
        context['apoderado_titular'] = self.object
        context['opciones_aula'] = BitacoraEstudiante._meta.get_field('aula').choices
        context['asignaturas'] = Asignatura.objects.all()
        context['profesionales'] = Profile.objects.all()
        context['estudiantes'] = Estudiante.objects.all()
        context['usuario_logueado'] = self.request.user  # Agrega el usuario logueado al contexto
        context['nivel_logro_choices'] = BitacoraEstudiante._meta.get_field('nivelLogro').choices
        context['fecha_actual'] = timezone.now().date()  # Agrega la fecha actual al contexto
        context['estudiante'] = get_object_or_404(Estudiante, id=self.kwargs['estudiante_id'])  # Recupera el estudiante según el ID
        return context
    
    def form_valid(self, form):
        form.instance.profesional = Profile.objects.get(user=self.request.user)  # Asigna el profesional como el usuario logueado
        form.instance.estudiante_id = self.kwargs['estudiante_id']  # Asigna el ID del estudiante al formulario
        messages.success(self.request, 'Bitácora registrada exitosamente')  # Mensaje de éxito
        return super().form_valid(form)  # Guarda la bitácora
    
    def form_invalid(self, form):
        messages.error(self.request, 'Error en el formulario, corrija los errores')  # Mensaje de error
        return super().form_invalid(form)  # Retorna el formulario

    def get_success_url(self):
        return reverse('bitacora_estudiante_list', kwargs={'estudiante_id': self.kwargs['estudiante_id']})
# -------------------------------------------------------------------------------------------------------------------

#LISTA DE BITÁCORAS DE ESTUDIANTES


# views.py
@add_group_name_to_context
class BitacoraEstudianteListView(UserPassesTestMixin, LoginRequiredMixin, ListView):
    model = BitacoraEstudiante
    template_name = 'informes/bitacoras_list.html'
    context_object_name = 'bitacoras'
    paginate_by = 6

    def test_func(self):
        return self.request.user.groups.exists()

    def handle_no_permission(self):
        return redirect('error')

    def get_queryset(self):
        estudiante_id = self.kwargs['estudiante_id']
        queryset = BitacoraEstudiante.objects.filter(estudiante_id=estudiante_id).order_by('-fecha')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        estudiante = get_object_or_404(Estudiante, id=self.kwargs['estudiante_id'])
        bitacoras = self.get_queryset()
        promedios_dia = PromedioDia.objects.filter(estudiante=estudiante).values('bitacora__fecha', 'total_dia')
        
        # Convertir los promedios a un diccionario para un acceso más fácil en el template
        promedios_dia_dict = {promedio['bitacora__fecha'].strftime('%Y-%m-%d'): promedio['total_dia'] for promedio in promedios_dia}
        
        context['profesionales'] = Profile.objects.all()
        context['estudiantes'] = Estudiante.objects.all()
        context['asignaturas'] = Asignatura.objects.all()
        context['estudiante'] = estudiante
        context['opciones_aula'] = BitacoraEstudiante._meta.get_field('aula').choices
        context['bitacoras'] = bitacoras
        context['bitacoras_json'] = json.dumps(list(bitacoras.values('id', 'actividad', 'fecha')), cls=DjangoJSONEncoder)
        context['promedios_dia_json'] = json.dumps(promedios_dia_dict, cls=DjangoJSONEncoder)
        context['usuario_logueado'] = self.request.user  # Agrega el usuario logueado al contexto
        context['nivel_logro_choices'] = BitacoraEstudiante._meta.get_field('nivelLogro').choices  # Agrega las opciones de nivel de logro al contexto
        return context
# -------------------------------------------------------------------------------------------------------------------


#VISTA BASADA EN CLASES PARA DETALLE DE UNA BITÁCORA DE UN ESTUDIANTE
@add_group_name_to_context
class BitacoraEstudianteDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = BitacoraEstudiante
    template_name = 'informes/bitacora_estudiante.html'
    context_object_name = 'bitacora'

    def test_func(self):
        return self.request.user.groups.exists()

    def handle_no_permission(self):
        return redirect('error')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bitacora = self.get_object()
        fecha_seleccionada = bitacora.fecha
        context['estudiante'] = bitacora.estudiante
        context['bitacoras'] = BitacoraEstudiante.objects.filter(estudiante=bitacora.estudiante, fecha=fecha_seleccionada)
        context['profesional'] = bitacora.profesional
        context['asignaturas'] = Asignatura.objects.all()
        context['logo_url'] = self.request.build_absolute_uri(static('Imagenes/LOGO LICEO TECNICO ADULTOS.jpg'))
        
        # Agregar el nombre del grupo en singular al contexto
        for bitacora in context['bitacoras']:
            bitacora.profesional.group_name_singular = plural_singular(bitacora.profesional.user.groups.first().name)
        
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'download' in request.GET:
            return self.download_pdf()
        return super().get(request, *args, **kwargs)

    def download_pdf(self):
        bitacora = self.get_object()
        context = self.get_context_data(object=bitacora)
        html_string = render_to_string('informes/bitacora_estudiante_pdf.html', context)
        html = HTML(string=html_string)
        pdf = html.write_pdf()

        estudiante = bitacora.estudiante
        fecha_actual = datetime.now().strftime('%Y-%m-%d')
        filename = f'bitacora_{estudiante.nombres}_{estudiante.apellido_paterno}_{estudiante.apellido_materno}_{fecha_actual}.pdf'

        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
# -------------------------------------------------------------------------------------------------------------------

#VISTA BASADA EN CLASES PARA EDITAR UNA BITÁCORA DE UN ESTUDIANTE
@add_group_name_to_context
class BitacoraEstudianteUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = BitacoraEstudiante
    template_name = 'informes/bitacora_estudiante_edit.html'
    form_class = BitacoraEstudianteForm
    success_url = reverse_lazy('bitacora_estudiante_list')  # Ajusta la URL de éxito según sea necesario

    def test_func(self):
        return self.request.user.groups.exists()

    def handle_no_permission(self):
        return redirect('error')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        groups = Group.objects.all()
        singular_groups = [plural_singular(group.name).capitalize() for group in groups]
        context['groups'] = zip(groups, singular_groups)
        context['asignaturas'] = Asignatura.objects.all()
        context['profesionales'] = Profile.objects.all()
        context['estudiantes'] = Estudiante.objects.all()
        context['opciones_aula'] = BitacoraEstudiante._meta.get_field('aula').choices
        context['usuario_logueado'] = self.request.user  # Agrega el usuario logueado al contexto
        context['estudiante'] = self.object.estudiante  # Recupera el estudiante relacionado con la bitácora
        context['bitacora'] = self.object  # Agrega la bitácora actual al contexto

        # Obtener todas las bitácoras del mismo día
        bitacoras_del_dia = BitacoraEstudiante.objects.filter(estudiante=self.object.estudiante, fecha=self.object.fecha).order_by('id')
        bitacora_index = list(bitacoras_del_dia).index(self.object)

        # Obtener la bitácora anterior y siguiente
        context['previous_bitacora'] = bitacoras_del_dia[bitacora_index - 1] if bitacora_index > 0 else None
        context['next_bitacora'] = bitacoras_del_dia[bitacora_index + 1] if bitacora_index < len(bitacoras_del_dia) - 1 else None

        # Agregar el índice del registro actual al contexto
        context['registro_numero'] = bitacora_index + 1

        return context

    def form_valid(self, form):
        messages.success(self.request, 'Bitácora actualizada exitosamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Por favor, corrija los errores en el formulario.')
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('bitacora_estudiante_list', kwargs={'estudiante_id': self.object.estudiante.id})


# -------------------------------------------------------------------------------------------------------------------
#VISTA REDIRECCIONAR LA BITACORA
@add_group_name_to_context
class BitacoraRedirectView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.groups.exists()

    def handle_no_permission(self):
        return redirect('error')

    def get(self, request, *args, **kwargs):
        fecha = request.GET.get('fecha')
        estudiante_id = kwargs.get('estudiante_id')
        bitacora = BitacoraEstudiante.objects.filter(estudiante_id=estudiante_id, fecha=fecha).first()
        if (bitacora):
            return redirect(reverse('bitacora_estudiante', kwargs={'pk': bitacora.pk}))
        else:
            messages.error(request, 'No se encontraron bitácoras para la fecha seleccionada.')
            return redirect('calendario_bitacoras')



# -------------------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------------------


# views.py
@add_group_name_to_context
class PromediosEstudianteView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Estudiante
    template_name = 'informes/promedios_estudiante.html'
    context_object_name = 'estudiante'

    def test_func(self):
        return self.request.user.groups.exists()

    def handle_no_permission(self):
        return redirect('error')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        estudiante = self.get_object()

        # Obtener el mes y año actual o el mes y año proporcionado en la URL
        mes_actual = int(self.request.GET.get('mes', timezone.now().month))
        ano_actual = int(self.request.GET.get('ano', timezone.now().year))

        # Convertir el número del mes al nombre del mes en español
        nombre_mes = format_date(timezone.datetime(ano_actual, mes_actual, 1), 'MMMM', locale='es')

        # Filtrar los promedios por el mes y año actual
        promedios_semanal = PromedioSemanalHistorico.objects.filter(
            estudiante=estudiante,
            inicio_semana__month=mes_actual,
            inicio_semana__year=ano_actual
        ).order_by('inicio_semana')

        # Filtrar los promedios mensuales para el mes actual
        promedios_mensual = PromedioMensualHistorico.objects.filter(
            estudiante=estudiante,
            inicio_mes__year=ano_actual,
            inicio_mes__month=mes_actual
        ).order_by('-inicio_mes')

        # Agrega la cantidad de bitácoras registradas, logradas y en vías de logro para cada semana y mes
        context['bitacoras_semanal'] = [
            {
                'id': promedio.id,
                'inicio_semana': promedio.inicio_semana,
                'fin_semana': promedio.fin_semana,
                'cantidad': BitacoraEstudiante.objects.filter(estudiante=estudiante, fecha__range=[promedio.inicio_semana, promedio.fin_semana]).count(),
                'logrados': BitacoraEstudiante.objects.filter(estudiante=estudiante, fecha__range=[promedio.inicio_semana, promedio.fin_semana], nivelLogro=True).count(),
                'vias_logro': BitacoraEstudiante.objects.filter(estudiante=estudiante, fecha__range=[promedio.inicio_semana, promedio.fin_semana], nivelLogro=False).count(),
                'promedio': promedio.promedio_semana
            }
            for promedio in promedios_semanal
        ]

        context['bitacoras_mensual'] = [
            {
                'id': promedio.id,
                'inicio_mes': promedio.inicio_mes,
                'fin_mes': promedio.fin_mes,
                'cantidad': BitacoraEstudiante.objects.filter(estudiante=estudiante, fecha__range=[promedio.inicio_mes, promedio.fin_mes]).count(),
                'logrados': BitacoraEstudiante.objects.filter(estudiante=estudiante, fecha__range=[promedio.inicio_mes, promedio.fin_mes], nivelLogro=True).count(),
                'vias_logro': BitacoraEstudiante.objects.filter(estudiante=estudiante, fecha__range=[promedio.inicio_mes, promedio.fin_mes], nivelLogro=False).count(),
                'promedio': promedio.promedio_mes
            }
            for promedio in promedios_mensual
        ]

        # Agregar el mes y año actual al contexto
        context['mes_actual'] = mes_actual
        context['ano_actual'] = ano_actual
        context['nombre_mes'] = nombre_mes

        # Agregar la primera semana y mes al contexto para el modal de edición
        if promedios_semanal:
            context['semana'] = promedios_semanal[0]
        if promedios_mensual:
            context['mes'] = promedios_mensual[0]

        return context

# ------------------------------------------------------------------------------------------------------------------   
#VISTAS PARA LOS INFORMES ANAMNESIS, PAI Y PACI
# -------------------------------------------------------------------------------------------------------------------
#VISTA BASADA EN CLASES PARA EDITAR UN ANAMNESIS POR EL ID DEL ESTUDIANTE
@add_group_name_to_context
class AnamnesisEstudianteUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = AnamnesisEstudiante
    template_name = 'informes/anamnesis_estudiante_edit.html'
    form_class = AnamnesisEstudianteForm

    # Solo los administradores, Coordinadores y Psicólogos pueden acceder a estas vistas
    def test_func(self):
        return self.request.user.groups.filter(name__in=['Administradores', 'Coordinadores', 'Coordinadores Suplentes', 'Psicólogos']).exists() 


    def handle_no_permission(self):
        return redirect('error')
    
    def get_object(self, queryset=None):
        estudiante_id = self.kwargs.get('pk')
        estudiante = get_object_or_404(Estudiante, id=estudiante_id)
        return get_object_or_404(AnamnesisEstudiante, estudiante=estudiante)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Datos básicos
        context.update({
            'regiones': Region.objects.all(),
            'comunas': Comuna.objects.all(),
            'estudiantes': Estudiante.objects.all(),
            'estudiante': get_object_or_404(Estudiante, id=self.kwargs['pk']),
            'anamnesis_estudiante': self.get_object(),
            'usuario_logueado': self.request.user,
        })
        
        # Opciones de los campos de selección
        context.update({
            'opciones_pais': AnamnesisEstudiante._meta.get_field('pais_natal').choices,
            'opciones_lengua': AnamnesisEstudiante._meta.get_field('lengua').choices,
            'opciones_sexo': AnamnesisEstudiante._meta.get_field('sexo').choices,
            'opciones_parentesco': Familiar._meta.get_field('parentesco').choices,
        })
        
        # Campos booleanos del modelo
        campos_booleanos = [
            'pediatria', 'kinesiologia', 'genetico', 'fonoaudiologia',
            'neurologia', 'psicologia', 'psiquiatria', 'psicopedagogia',
            'terapia_ocupacional', 'otro', 'perdida_auditiva',
            'perdida_visual', 'motor', 'paraplejia', 'trastorno_conductual'
        ]
        for campo in campos_booleanos:
            context[campo] = getattr(self.object, campo)
        
        context['otros'] = self.object.otros
        context['alumno_trabajador'] = self.object.alumno_trabajador

        # Convertir nombre del grupo a singular
        grupo_plural = self.request.user.groups.first().name
        grupo_singular = plural_singular(grupo_plural)
        context['cargo'] = grupo_singular

        # Manejo del formset de familiares
        if self.request.POST:
            context['familiar_formset'] = FamiliarFormSet(
                self.request.POST,
                instance=self.object
            )
        else:
            context['familiar_formset'] = FamiliarFormSet(
                instance=self.object
            )
        context['logo_liceo_url'] = self.request.build_absolute_uri(static('Imagenes/LOGO LICEO TECNICO ADULTOS.jpg'))
        context['logo_servicio_url'] = self.request.build_absolute_uri(static('Imagenes/Servicio_local.jpg'))
        context['logo_pie_url'] = self.request.build_absolute_uri(static('Imagenes/Imagen_PIE.jpg'))
        
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        familiar_formset = context['familiar_formset']
        
        with transaction.atomic():
            try:
                # Validar y guardar el formulario principal
                self.object = form.save(commit=False)
                self.object.entrevistador = self.request.user.profile
                self.object.save()
                
                # Validar y guardar el formset de familiares
                if familiar_formset.is_valid():
                    familiar_formset.save()
                    messages.success(self.request, 'Anamnesis actualizada exitosamente.')
                    return redirect(self.get_success_url())
                else:
                    return self.form_invalid(form)
                    
            except Exception as e:
                return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Por favor, corrija los errores en el formulario.')
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('estudiante', kwargs={'pk': self.object.estudiante.pk})

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'download' in request.GET:
            return self.download_pdf()
        return super().get(request, *args, **kwargs)

    def download_pdf(self):
        anamnesis = self.get_object()
        context = self.get_context_data(object=anamnesis)
        html_string = render_to_string('informes/anamnesis_estudiante_pdf.html', context)
        html = HTML(string=html_string)
        pdf = html.write_pdf()

        estudiante = anamnesis.estudiante
        fecha_actual = datetime.now().strftime('%Y-%m-%d')
        filename = f'Anamnesis_{estudiante.nombres}_{estudiante.apellido_paterno}_{estudiante.apellido_materno}_{fecha_actual}.pdf'

        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    


# -------------------------------------------------------------------------------------------------------------------
#VISTA BASADA EN CLASES PARA EDITAR UN PAI POR EL ID DEL ESTUDIANTE

@add_group_name_to_context
class PaiEstudianteUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Pai
    template_name = 'informes/pai_estudiante_edit.html'
    form_class = PaiEstudianteForm

    # Solo los administradores, Coordinadores y Psicólogos pueden acceder a estas vistas
    def test_func(self):
        return self.request.user.groups.filter(name__in=['Administradores', 'Coordinadores', 'Coordinadores Suplentes', 'Psicólogos']).exists() 

    def handle_no_permission(self):
        return redirect('error')
    
    def get_object(self, queryset=None):
        estudiante_id = self.kwargs.get('pk')
        estudiante = get_object_or_404(Estudiante, id=estudiante_id)
        return get_object_or_404(Pai, estudiante=estudiante)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pai = self.get_object()
        
        # Filtrar solo los coordinadores
        coordinadores_group = Group.objects.get(name='Coordinadores')
        coordinadores = Profile.objects.filter(user__groups=coordinadores_group)
        
        # Datos básicos
        context.update({
            'regiones': Region.objects.all(),
            'comunas': Comuna.objects.all(),
            'estudiantes': Estudiante.objects.all(),
            'coordinadores': coordinadores,  # Pasar solo los coordinadores al contexto
            'estudiante': pai.estudiante,
            'pai': pai,
            'usuario_logueado': self.request.user,
        })
        
        # Opciones de los campos de selección
        context.update({
            'opciones_sexo': Pai._meta.get_field('sexo').choices,
            'opciones_parentesco': Familia._meta.get_field('parentesco').choices,
            'opciones_docente': Docentes._meta.get_field('profesion').choices,
        })

        # Manejo de los formsets
        if self.request.POST:
            context['equipo_responsable_formset'] = EquipoResponsablePaiFormSet(self.request.POST, instance=pai)
            context['docentes_formset'] = DocentesFormSet(self.request.POST, instance=pai)
            context['familia_formset'] = FamiliaFormSet(self.request.POST, instance=pai)
            context['estrategias_diversificadas_formset'] = EstrategiasDiversificadasFormSet(self.request.POST, instance=pai)
            context['apoyos_especializados_formset'] = ApoyosEspecializadosFormSet(self.request.POST, instance=pai)
            context['horario_apoyos_formset'] = HorarioApoyosFormSet(self.request.POST, instance=pai)
            context['firma_formset'] = FirmaFormSet(self.request.POST, instance=pai)
        else:
            context['equipo_responsable_formset'] = EquipoResponsablePaiFormSet(instance=pai)
            context['docentes_formset'] = DocentesFormSet(instance=pai)
            context['familia_formset'] = FamiliaFormSet(instance=pai)
            context['estrategias_diversificadas_formset'] = EstrategiasDiversificadasFormSet(instance=pai)
            context['apoyos_especializados_formset'] = ApoyosEspecializadosFormSet(instance=pai)
            context['horario_apoyos_formset'] = HorarioApoyosFormSet(instance=pai)
            context['firma_formset'] = FirmaFormSet(instance=pai)
        
        context['logo_liceo_url'] = self.request.build_absolute_uri(static('Imagenes/LOGO LICEO TECNICO ADULTOS.jpg'))
        context['logo_servicio_url'] = self.request.build_absolute_uri(static('Imagenes/Servicio_local.jpg'))
        context['logo_pie_url'] = self.request.build_absolute_uri(static('Imagenes/Imagen_PIE.jpg'))
        
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        equipo_responsable_formset = context['equipo_responsable_formset']
        docentes_formset = context['docentes_formset']
        familia_formset = context['familia_formset']
        estrategias_diversificadas_formset = context['estrategias_diversificadas_formset']
        apoyos_especializados_formset = context['apoyos_especializados_formset']
        horario_apoyos_formset = context['horario_apoyos_formset']
        firma_formset = context['firma_formset']
        
        with transaction.atomic():
            try:
                # Validar y guardar el formulario principal
                self.object = form.save(commit=False)
                self.object.save()
                
                # Validar y guardar los formsets
                if (equipo_responsable_formset.is_valid() and docentes_formset.is_valid() and
                    familia_formset.is_valid() and estrategias_diversificadas_formset.is_valid() and
                    apoyos_especializados_formset.is_valid() and horario_apoyos_formset.is_valid() and
                    firma_formset.is_valid()):
                    
                    equipo_responsable_formset.instance = self.object
                    equipo_responsable_formset.save()
                    docentes_formset.instance = self.object
                    docentes_formset.save()
                    familia_formset.instance = self.object
                    familia_formset.save()
                    estrategias_diversificadas_formset.instance = self.object
                    estrategias_diversificadas_formset.save()
                    apoyos_especializados_formset.instance = self.object
                    apoyos_especializados_formset.save()
                    horario_apoyos_formset.instance = self.object
                    horario_apoyos_formset.save()
                    firma_formset.instance = self.object
                    firma_formset.save()
                    
                    messages.success(self.request, 'PAI actualizado exitosamente.')
                    return redirect(self.get_success_url())
                else:
                    # Mostrar errores de los formsets
                    for formset in [equipo_responsable_formset, docentes_formset, familia_formset, estrategias_diversificadas_formset, apoyos_especializados_formset, horario_apoyos_formset, firma_formset]:
                        for form in formset:
                            for field in form:
                                for error in field.errors:
                                    messages.error(self.request, f"Error en {field.label}: {error}")
                    return self.form_invalid(form)
                    
            except Exception as e:
                messages.error(self.request, f'Error al actualizar el PAI: {e}')
                return self.form_invalid(form)

    def form_invalid(self, form):
        context = self.get_context_data()
        context['form'] = form
        messages.error(self.request, 'Por favor, corrija los errores en el formulario.')
        return self.render_to_response(context)
    
    def get_success_url(self):
        return reverse('estudiante', kwargs={'pk': self.object.estudiante.pk})
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'download' in request.GET:
            return self.download_pdf()
        return super().get(request, *args, **kwargs)
    
    def download_pdf(self):
        pai = self.get_object()
        context = self.get_context_data(object=pai)
        html_string = render_to_string('informes/pai_estudiante_pdf.html', context)
        html = HTML(string=html_string)
        pdf = html.write_pdf()

        estudiante = pai.estudiante
        fecha_actual = datetime.now().strftime('%Y-%m-%d')
        filename = f'PAI_{estudiante.nombres}_{estudiante.apellido_paterno}_{estudiante.apellido_materno}_{fecha_actual}.pdf'

        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    

#_-------------------------------------------------------------------------------------------------------------------
# VISTA BASADA EN CLASES PARA EDITAR UN PACI POR EL ID DEL ESTUDIANTE

@add_group_name_to_context
class PaciEstudianteUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Paci
    template_name = 'informes/paci_estudiante_edit.html'
    form_class = PaciForm

    # Solo los administradores, Coordinadores y Psicólogos pueden acceder a estas vistas
    def test_func(self):
        return self.request.user.groups.filter(name__in=['Administradores', 'Coordinadores', 'Coordinadores Suplentes', 'Psicólogos']).exists() 

    def handle_no_permission(self):
        return redirect('error')
    
    def get_object(self, queryset=None):
        estudiante_id = self.kwargs.get('pk')
        estudiante = get_object_or_404(Estudiante, id=estudiante_id)
        return get_object_or_404(Paci, estudiante=estudiante)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paci = self.get_object()
        
        # Filtrar solo los coordinadores
        coordinadores_group = Group.objects.get(name='Coordinadores')
        coordinadores = Profile.objects.filter(user__groups=coordinadores_group)
        
        # Obtener el apoderado del estudiante
        apoderado = ApoderadoTitular.objects.filter(estudiante=paci.estudiante).first()
        
        # Datos básicos
        context.update({
            'regiones': Region.objects.all(),
            'comunas': Comuna.objects.all(),
            'estudiantes': Estudiante.objects.all(),
            'coordinadores': coordinadores,
            'estudiante': paci.estudiante,
            'paci': paci,
            'usuario_logueado': self.request.user,
            'apoderado': apoderado,  # Agregar el apoderado al contexto
        })
        
        # Opciones de los campos de selección
        context.update({
            'opciones_sexo': Paci._meta.get_field('sexo').choices,
            'opciones_parentesco': Familia._meta.get_field('parentesco').choices,
            'opciones_docente': Docentes._meta.get_field('profesion').choices,
        })

        # Manejo de los formsets
        if self.request.POST:
            context['equipo_responsable_formset'] = EquipoResponsablePaciFormSet(self.request.POST, instance=paci)
            context['aula_recursos_formset'] = AulaRecursosFormSet(self.request.POST, instance=paci)
            context['aula_regular_formset'] = AulaRegularFormSet(self.request.POST, instance=paci)
            context['presentacion_representacion_formset'] = PresentacionRepresentacionFormSet(self.request.POST, instance=paci)
            context['medios_ejecucion_expresion_formset'] = MediosEjecucionExpresionFormSet(self.request.POST, instance=paci)
            context['multiples_medios_formset'] = MultiplesMediosFormSet(self.request.POST, instance=paci)
            context['entorno_formset'] = EntornoFormSet(self.request.POST, instance=paci)
            context['organizacion_tiempo_formset'] = OrganizacionTiempoFormSet(self.request.POST, instance=paci)
            context['graduacion_complejidad_formset'] = GraduacionComplejidadFormSet(self.request.POST, instance=paci)
            context['priorizacion_oa_formset'] = PriorizacionOAFormSet(self.request.POST, instance=paci)
            context['temporalizacion_formset'] = TemporalizacionFormSet(self.request.POST, instance=paci)
            context['enriquecimiento_curriculum_formset'] = EnriquecimientoCurriculumFormSet(self.request.POST, instance=paci)
            context['objetivos_aprendizaje_formset'] = ObjetivosAprendizajeFormSet(self.request.POST, instance=paci)
            context['columnas_objetivos_aprendizaje_formset'] = ColumnasObjetivosAprendizajeFormSet(self.request.POST, instance=paci)
            context['colaboracion_familia_formset'] = ColaboracionFamiliaFormSet(self.request.POST, instance=paci)
            context['crit_evaluacion_promocion_formset'] = CritEvaluacionPromocionFormSet(self.request.POST, instance=paci)
            context['seguimiento_paci_formset'] = SeguimientoPaciFormSet(self.request.POST, instance=paci)
            context['firma_paci_formset'] = FirmaPaciFormSet(self.request.POST, instance=paci)
        else:
            context['equipo_responsable_formset'] = EquipoResponsablePaciFormSet(instance=paci)
            context['aula_recursos_formset'] = AulaRecursosFormSet(instance=paci)
            context['aula_regular_formset'] = AulaRegularFormSet(instance=paci)
            context['presentacion_representacion_formset'] = PresentacionRepresentacionFormSet(instance=paci)
            context['medios_ejecucion_expresion_formset'] = MediosEjecucionExpresionFormSet(instance=paci)
            context['multiples_medios_formset'] = MultiplesMediosFormSet(instance=paci)
            context['entorno_formset'] = EntornoFormSet(instance=paci)
            context['organizacion_tiempo_formset'] = OrganizacionTiempoFormSet(instance=paci)
            context['graduacion_complejidad_formset'] = GraduacionComplejidadFormSet(instance=paci)
            context['priorizacion_oa_formset'] = PriorizacionOAFormSet(instance=paci)
            context['temporalizacion_formset'] = TemporalizacionFormSet(instance=paci)
            context['enriquecimiento_curriculum_formset'] = EnriquecimientoCurriculumFormSet(instance=paci)
            context['objetivos_aprendizaje_formset'] = ObjetivosAprendizajeFormSet(instance=paci)
            context['columnas_objetivos_aprendizaje_formset'] = ColumnasObjetivosAprendizajeFormSet(instance=paci)
            context['colaboracion_familia_formset'] = ColaboracionFamiliaFormSet(instance=paci)
            context['crit_evaluacion_promocion_formset'] = CritEvaluacionPromocionFormSet(instance=paci)
            context['seguimiento_paci_formset'] = SeguimientoPaciFormSet(instance=paci)
            context['firma_paci_formset'] = FirmaPaciFormSet(instance=paci)
        
        context['logo_liceo_url'] = self.request.build_absolute_uri(static('Imagenes/LOGO LICEO TECNICO ADULTOS.jpg'))
        context['logo_servicio_url'] = self.request.build_absolute_uri(static('Imagenes/Servicio_local.jpg'))
        context['logo_pie_url'] = self.request.build_absolute_uri(static('Imagenes/Imagen_PIE.jpg'))
        
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        equipo_responsable_formset = context['equipo_responsable_formset']
        aula_recursos_formset = context['aula_recursos_formset']
        aula_regular_formset = context['aula_regular_formset']
        presentacion_representacion_formset = context['presentacion_representacion_formset']
        medios_ejecucion_expresion_formset = context['medios_ejecucion_expresion_formset']
        multiples_medios_formset = context['multiples_medios_formset']
        entorno_formset = context['entorno_formset']
        organizacion_tiempo_formset = context['organizacion_tiempo_formset']
        graduacion_complejidad_formset = context['graduacion_complejidad_formset']
        priorizacion_oa_formset = context['priorizacion_oa_formset']
        temporalizacion_formset = context['temporalizacion_formset']
        enriquecimiento_curriculum_formset = context['enriquecimiento_curriculum_formset']
        objetivos_aprendizaje_formset = context['objetivos_aprendizaje_formset']
        columnas_objetivos_aprendizaje_formset = context['columnas_objetivos_aprendizaje_formset']
        colaboracion_familia_formset = context['colaboracion_familia_formset']
        crit_evaluacion_promocion_formset = context['crit_evaluacion_promocion_formset']
        seguimiento_paci_formset = context['seguimiento_paci_formset']
        firma_paci_formset = context['firma_paci_formset']
        
        with transaction.atomic():
            try:
                # Validar y guardar el formulario principal
                self.object = form.save(commit=False)
                self.object.save()
                
                # Validar y guardar los formsets
                if (equipo_responsable_formset.is_valid() and aula_recursos_formset.is_valid() and
                    aula_regular_formset.is_valid() and presentacion_representacion_formset.is_valid() and
                    medios_ejecucion_expresion_formset.is_valid() and multiples_medios_formset.is_valid() and
                    entorno_formset.is_valid() and organizacion_tiempo_formset.is_valid() and
                    graduacion_complejidad_formset.is_valid() and priorizacion_oa_formset.is_valid() and
                    temporalizacion_formset.is_valid() and enriquecimiento_curriculum_formset.is_valid() and
                    objetivos_aprendizaje_formset.is_valid() and columnas_objetivos_aprendizaje_formset.is_valid() and
                    colaboracion_familia_formset.is_valid() and crit_evaluacion_promocion_formset.is_valid() and
                    seguimiento_paci_formset.is_valid() and firma_paci_formset.is_valid()):
                    
                    equipo_responsable_formset.instance = self.object
                    equipo_responsable_formset.save()
                    aula_recursos_formset.instance = self.object
                    aula_recursos_formset.save()
                    aula_regular_formset.instance = self.object
                    aula_regular_formset.save()
                    presentacion_representacion_formset.instance = self.object
                    presentacion_representacion_formset.save()
                    medios_ejecucion_expresion_formset.instance = self.object
                    medios_ejecucion_expresion_formset.save()
                    multiples_medios_formset.instance = self.object
                    multiples_medios_formset.save()
                    entorno_formset.instance = self.object
                    entorno_formset.save()
                    organizacion_tiempo_formset.instance = self.object
                    organizacion_tiempo_formset.save()
                    graduacion_complejidad_formset.instance = self.object
                    graduacion_complejidad_formset.save()
                    priorizacion_oa_formset.instance = self.object
                    priorizacion_oa_formset.save()
                    temporalizacion_formset.instance = self.object
                    temporalizacion_formset.save()
                    enriquecimiento_curriculum_formset.instance = self.object
                    enriquecimiento_curriculum_formset.save()
                    objetivos_aprendizaje_formset.instance = self.object
                    objetivos_aprendizaje_formset.save()
                    columnas_objetivos_aprendizaje_formset.instance = self.object
                    columnas_objetivos_aprendizaje_formset.save()
                    colaboracion_familia_formset.instance = self.object
                    colaboracion_familia_formset.save()
                    crit_evaluacion_promocion_formset.instance = self.object
                    crit_evaluacion_promocion_formset.save()
                    seguimiento_paci_formset.instance = self.object
                    seguimiento_paci_formset.save()
                    firma_paci_formset.instance = self.object
                    firma_paci_formset.save()
                    
                    messages.success(self.request, 'PACI actualizado exitosamente.')
                    return redirect(self.get_success_url())
                else:
                    # Mostrar errores de los formsets
                    for formset in [equipo_responsable_formset, aula_recursos_formset, aula_regular_formset, presentacion_representacion_formset, medios_ejecucion_expresion_formset, multiples_medios_formset, entorno_formset, organizacion_tiempo_formset, graduacion_complejidad_formset, priorizacion_oa_formset, temporalizacion_formset, enriquecimiento_curriculum_formset, objetivos_aprendizaje_formset, columnas_objetivos_aprendizaje_formset, colaboracion_familia_formset, crit_evaluacion_promocion_formset, seguimiento_paci_formset, firma_paci_formset]:
                        for form in formset:
                            for field in form:
                                for error in field.errors:
                                    messages.error(self.request, f"Error en {field.label}: {error}")
                    return self.form_invalid(form)
                    
            except Exception as e:
                messages.error(self.request, f'Error al actualizar el PACI: {e}')
                return self.form_invalid(form)

    def form_invalid(self, form):
        context = self.get_context_data()
        context['form'] = form
        messages.error(self.request, 'Por favor, corrija los errores en el formulario.')
        return self.render_to_response(context)

    def get_success_url(self):
        return reverse('estudiante', kwargs={'pk': self.object.estudiante.pk})

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'download' in request.GET:
            return self.download_pdf()
        return super().get(request, *args, **kwargs)
    
    def download_pdf(self):
        paci = self.get_object()
        context = self.get_context_data(object=paci)
        html_string = render_to_string('informes/paci_estudiante_pdf.html', context)
        html = HTML(string=html_string)
        pdf = html.write_pdf()

        estudiante = paci.estudiante
        fecha_actual = datetime.now().strftime('%Y-%m-%d')
        filename = f'PACI_{estudiante.nombres}_{estudiante.apellido_paterno}_{estudiante.apellido_materno}_{fecha_actual}.pdf'

        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response