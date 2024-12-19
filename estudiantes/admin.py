"""
Autores:
- Raúl Córdova Vicencio
- Francisca Olavarría Pavez
- Carlos Olivero Bruno
Fecha: 01 diciembre 2024
"""

from django.contrib import admin
from .models import AreaAcademica, Asignatura, BitacoraEstudiante, Curso, Estudiante\
    , ApoderadoTitular, PromedioDia, PromedioSemanalHistorico, PromedioMensualHistorico\
    , AnamnesisEstudiante, Familiar, Pai, EquipoResponsablePai, Docentes, Familia\
    , EstrategiasDiversificadas, ApoyosEspecializados, HorarioApoyos, Firma

# Registrar modelo Área Académica
class AreaAcademicaAdmin(admin.ModelAdmin):
    """
    Admin para el modelo Área Académica.
    """
    list_display = ['nombre']
    search_fields = ['nombre']

admin.site.register(AreaAcademica, AreaAcademicaAdmin)

# Registrar modelo Curso
class CursoAdmin(admin.ModelAdmin):
    """
    Admin para el modelo Curso.
    """
    list_display = ['area_academica', 'nombre']
    search_fields = ['area_academica', 'nombre']

admin.site.register(Curso, CursoAdmin)

# Registrar modelo Asignatura
class AsignaturaAdmin(admin.ModelAdmin):
    """
    Admin para el modelo Asignatura.
    """
    list_display = ['asignatura']
    search_fields = ['asignatura']

admin.site.register(Asignatura, AsignaturaAdmin)

# Registrar Bitácora Estudiante
class BitacoraEstudianteAdmin(admin.ModelAdmin):
    """
    Admin para el modelo Bitácora Estudiante.
    """
    list_display = ['profesional', 'estudiante', 'fecha', 'horas_estudiante', 'aula', 'asignatura', 'actividad', 'observaciones', 'nivelLogro']
    search_fields = ['estudiante', 'asignatura', 'actividad']
    fieldsets = (
        ('1. IDENTIFICACIÓN DEL ESTUDIANTE', {
            'fields': ('profesional', 'estudiante', 'fecha', 'horas_estudiante', 'aula', 'asignatura', 'actividad', 'observaciones', 'nivelLogro'),
        }),
    )

admin.site.register(BitacoraEstudiante, BitacoraEstudianteAdmin)

# Registrar Estudiante
class EstudianteAdmin(admin.ModelAdmin):
    """
    Admin para el modelo Estudiante.
    """
    list_display = ('nee', 'cursos', 'get_area_academica', 'rut', 'nombres', 'apellido_paterno', 'apellido_materno', 'fecha_nacimiento', 'direccion', 'telefono', 'correo', 'region', 'comuna', 'etnia', 'comorbilidad')
    search_fields = ['nombres', 'apellido_paterno', 'apellido_materno', 'rut']
    readonly_fields = ('get_area_academica',)
    fieldsets = (
        (None, {
            'fields': ('nee', 'cursos', 'rut', 'nombres', 'apellido_paterno', 'apellido_materno', 'fecha_nacimiento', 'direccion', 'telefono', 'correo', 'region', 'comuna', 'etnia', 'comorbilidad'),
        }),
        ('Información del Curso', {
            'fields': ('get_area_academica',),
        }),
    )

    def get_area_academica(self, obj):
        """
        Obtiene el nombre del área académica del curso del estudiante.
        """
        return obj.cursos.area_academica.nombre
    get_area_academica.short_description = 'Área Académica'
    get_area_academica.admin_order_field = 'cursos__area_academica__nombre'

admin.site.register(Estudiante, EstudianteAdmin)

# Registrar Apoderado Titular
class ApoderadoTitularAdmin(admin.ModelAdmin):
    """
    Admin para el modelo Apoderado Titular.
    """
    list_display = ('estudiante', 'rut', 'nombres', 'apellido_paterno', 'apellido_materno', 'fecha_nacimiento', 'direccion', 'telefono', 'email', 'region', 'comuna', 'etnia', 'salud', 'renta')

admin.site.register(ApoderadoTitular, ApoderadoTitularAdmin)

# Registrar PromedioDia
class PromedioDiaAdmin(admin.ModelAdmin):
    """
    Admin para el modelo PromedioDia.
    """
    list_display = ('estudiante', 'bitacora', 'total_dia')
    search_fields = ['estudiante__nombres', 'estudiante__apellido_paterno', 'estudiante__apellido_materno']

admin.site.register(PromedioDia, PromedioDiaAdmin)

# Registrar PromedioSemanalHistorico
class PromedioSemanalHistoricoAdmin(admin.ModelAdmin):
    """
    Admin para el modelo PromedioSemanalHistorico.
    """
    list_display = ('estudiante', 'inicio_semana', 'fin_semana', 'promedio_semana')
    search_fields = ['estudiante__nombres', 'estudiante__apellido_paterno', 'estudiante__apellido_materno']

admin.site.register(PromedioSemanalHistorico, PromedioSemanalHistoricoAdmin)

# Registrar PromedioMensualHistorico
class PromedioMensualHistoricoAdmin(admin.ModelAdmin):
    """
    Admin para el modelo PromedioMensualHistorico.
    """
    list_display = ('estudiante', 'inicio_mes', 'fin_mes', 'promedio_mes')
    search_fields = ['estudiante__nombres', 'estudiante__apellido_paterno', 'estudiante__apellido_materno']

admin.site.register(PromedioMensualHistorico, PromedioMensualHistoricoAdmin)

# Registrar modelo Familiar en línea
class FamiliarInline(admin.TabularInline):
    """
    Inline admin para el modelo Familiar.
    """
    model = Familiar
    extra = 1

# Registrar modelo AnamnesisEstudiante
class AnamnesisEstudianteAdmin(admin.ModelAdmin):
    """
    Admin para el modelo AnamnesisEstudiante.
    """
    list_display = ['estudiante', 'fecha_entrevista', 'curso_actual', 'edad', 'pais_natal', 'sexo', 'lengua', 'alumno_trabajador']
    search_fields = ['estudiante__nombres', 'estudiante__apellido_paterno', 'estudiante__apellido_materno', 'curso_actual__nombre']
    inlines = [FamiliarInline]
    fieldsets = (
        ('1. IDENTIFICACIÓN DEL ESTUDIANTE', {
            'fields': ('estudiante', 'curso_actual', 'edad', 'pais_natal', 'sexo', 'lengua', 'alumno_trabajador'),
        }),
        ('2. IDENTIFICACIÓN DEL ENTREVISTADOR', {
            'fields': ('entrevistador', 'fecha_entrevista'),
        }),
        ('3. DEFINICIÓN DEL PROBLEMA O SITUACIÓN QUE MOTIVA LA ENTREVISTA', {
            'fields': ('definicion_problema',),
        }),
        ('4. ANTECEDENTES RELATIVOS AL DESARROLLO Y A LA SALUD DEL/LA ESTUDIANTE', {
            'fields': ('pediatria', 'kinesiologia', 'genetico', 'fonoaudiologia', 'neurologia', 'psicologia', 'psiquiatria', 'psicopedagogia', 'terapia_ocupacional', 'otro'),
        }),
        ('5. SÍNTESIS DE LOS ANTECEDENTES DE SALUD, ESCOLARES Y SOCIALES DEL ESTUDIANTE', {
            'fields': ('perdida_auditiva', 'perdida_visual', 'motor', 'paraplejia', 'trastorno_conductual', 'otros'),
        }),
        ('OBSERVACIONES', {
            'fields': ('observaciones',),
        }),
    )

admin.site.register(AnamnesisEstudiante, AnamnesisEstudianteAdmin)

# REGISTRAR EL MODELO PAI
from django.contrib import admin
from .models import Pai, EquipoResponsablePai, Docentes, Familia, EstrategiasDiversificadas, ApoyosEspecializados, HorarioApoyos, Firma

# Registrar modelos en línea
class EquipoResponsablePaiInline(admin.TabularInline):
    """
    Inline admin para el modelo EquipoResponsablePai.
    """
    model = EquipoResponsablePai
    extra = 1

class DocentesInline(admin.TabularInline):
    """
    Inline admin para el modelo Docentes.
    """
    model = Docentes
    extra = 1

class FamiliaInline(admin.TabularInline):
    """
    Inline admin para el modelo Familia.
    """
    model = Familia
    extra = 1

class EstrategiasDiversificadasInline(admin.TabularInline):
    """
    Inline admin para el modelo EstrategiasDiversificadas.
    """
    model = EstrategiasDiversificadas
    extra = 1

class ApoyosEspecializadosInline(admin.TabularInline):
    """
    Inline admin para el modelo ApoyosEspecializados.
    """
    model = ApoyosEspecializados
    extra = 1

class HorarioApoyosInline(admin.TabularInline):
    """
    Inline admin para el modelo HorarioApoyos.
    """
    model = HorarioApoyos
    extra = 1

class FirmaInline(admin.TabularInline):
    """
    Inline admin para el modelo Firma.
    """
    model = Firma
    extra = 1

# Registrar modelo Pai
class PaiAdmin(admin.ModelAdmin):
    """
    Admin para el modelo Pai.
    """
    list_display = ['estudiante', 'curso', 'sexo', 'edad', 'fecha_elaboracion']
    search_fields = ['estudiante__nombres', 'estudiante__apellido_paterno', 'estudiante__apellido_materno', 'curso__nombre']
    inlines = [EquipoResponsablePaiInline, DocentesInline, FamiliaInline, EstrategiasDiversificadasInline, ApoyosEspecializadosInline, HorarioApoyosInline, FirmaInline]
    fieldsets = (
        ('1. IDENTIFICACIÓN DEL ESTUDIANTE', {
            'fields': ('estudiante', 'curso', 'sexo', 'edad', 'fecha_elaboracion'),
        }),
        ('2. IDENTIFICACIÓN DEL ESTABLECIMIENTO', {
            'fields': ('rbd', 'nombre_establecimiento', 'region', 'comuna', 'coordinador_pie'),
        }),
    )

admin.site.register(Pai, PaiAdmin)

from django.contrib import admin
from .models import Paci, EquipoResponsablePaci, AulaRecursos, AulaRegular, PresentacionRepresentacion, MediosEjecucionExpresion, MultiplesMedios, Entorno, OrganizacionTiempo, GraduacionComplejidad, PriorizacionOA, Temporalizacion, EnriquecimientoCurriculum, ObjetivosAprendizaje, ColumnasObjetivosAprendizaje, ColaboracionFamilia, CritEvaluacionPromocion, SeguimientoPaci, FirmaPaci

# Registrar modelos en línea
class EquipoResponsablePaciInline(admin.TabularInline):
    """
    Inline admin para el modelo EquipoResponsablePaci.
    """
    model = EquipoResponsablePaci
    extra = 1

class AulaRecursosInline(admin.TabularInline):
    """
    Inline admin para el modelo AulaRecursos.
    """
    model = AulaRecursos
    extra = 1

class AulaRegularInline(admin.TabularInline):
    """
    Inline admin para el modelo AulaRegular.
    """
    model = AulaRegular
    extra = 1

class PresentacionRepresentacionInline(admin.TabularInline):
    """
    Inline admin para el modelo PresentacionRepresentacion.
    """
    model = PresentacionRepresentacion
    extra = 1

class MediosEjecucionExpresionInline(admin.TabularInline):
    """
    Inline admin para el modelo MediosEjecucionExpresion.
    """
    model = MediosEjecucionExpresion
    extra = 1

class MultiplesMediosInline(admin.TabularInline):
    """
    Inline admin para el modelo MultiplesMedios.
    """
    model = MultiplesMedios
    extra = 1

class EntornoInline(admin.TabularInline):
    """
    Inline admin para el modelo Entorno.
    """
    model = Entorno
    extra = 1

class OrganizacionTiempoInline(admin.TabularInline):
    """
    Inline admin para el modelo OrganizacionTiempo.
    """
    model = OrganizacionTiempo
    extra = 1

class GraduacionComplejidadInline(admin.TabularInline):
    """
    Inline admin para el modelo GraduacionComplejidad.
    """
    model = GraduacionComplejidad
    extra = 1

class PriorizacionOAInline(admin.TabularInline):
    """
    Inline admin para el modelo PriorizacionOA.
    """
    model = PriorizacionOA
    extra = 1

class TemporalizacionInline(admin.TabularInline):
    """
    Inline admin para el modelo Temporalizacion.
    """
    model = Temporalizacion
    extra = 1

class EnriquecimientoCurriculumInline(admin.TabularInline):
    """
    Inline admin para el modelo EnriquecimientoCurriculum.
    """
    model = EnriquecimientoCurriculum
    extra = 1

class ObjetivosAprendizajeInline(admin.TabularInline):
    """
    Inline admin para el modelo ObjetivosAprendizaje.
    """
    model = ObjetivosAprendizaje
    extra = 1

class ColumnasObjetivosAprendizajeInline(admin.TabularInline):
    """
    Inline admin para el modelo ColumnasObjetivosAprendizaje.
    """
    model = ColumnasObjetivosAprendizaje
    extra = 1

class ColaboracionFamiliaInline(admin.TabularInline):
    """
    Inline admin para el modelo ColaboracionFamilia.
    """
    model = ColaboracionFamilia
    extra = 1

class CritEvaluacionPromocionInline(admin.TabularInline):
    """
    Inline admin para el modelo CritEvaluacionPromocion.
    """
    model = CritEvaluacionPromocion
    extra = 1

class SeguimientoPaciInline(admin.TabularInline):
    """
    Inline admin para el modelo SeguimientoPaci.
    """
    model = SeguimientoPaci
    extra = 1

class FirmaPaciInline(admin.TabularInline):
    """
    Inline admin para el modelo FirmaPaci.
    """
    model = FirmaPaci
    extra = 1

# Registrar modelo Paci
class PaciAdmin(admin.ModelAdmin):
    """
    Admin para el modelo Paci.
    """
    list_display = ['estudiante', 'curso', 'sexo', 'edad', 'fecha_elaboracion']
    search_fields = ['estudiante__nombres', 'estudiante__apellido_paterno', 'estudiante__apellido_materno', 'curso__nombre']
    inlines = [EquipoResponsablePaciInline, AulaRecursosInline, AulaRegularInline, PresentacionRepresentacionInline, MediosEjecucionExpresionInline, MultiplesMediosInline, EntornoInline, OrganizacionTiempoInline, GraduacionComplejidadInline, PriorizacionOAInline, TemporalizacionInline, EnriquecimientoCurriculumInline, ObjetivosAprendizajeInline, ColumnasObjetivosAprendizajeInline, ColaboracionFamiliaInline, CritEvaluacionPromocionInline, SeguimientoPaciInline, FirmaPaciInline]
    fieldsets = (
        ('1. IDENTIFICACIÓN DEL ESTUDIANTE', {
            'fields': ('estudiante', 'curso', 'sexo', 'edad', 'fecha_elaboracion', 'fecha_revision', 'duracion', 'antecedentes_salud', 'antecedentes_escolares', 'antecedentes_familiares', 'expectativas', 'apoyos'),
        }),
        ('2. IDENTIFICACIÓN DEL ESTABLECIMIENTO', {
            'fields': ('rbd', 'nombre_establecimiento', 'region', 'comuna', 'coordinador_pie', 'jefe_utp'),
        }),
    )

admin.site.register(Paci, PaciAdmin)