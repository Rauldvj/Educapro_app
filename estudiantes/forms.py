"""
Autores:
- Raúl Córdova Vicencio
- Francisca Olavarría Pavez
- Carlos Olivero Bruno
Fecha: 01 diciembre 2024
"""

from datetime import datetime
from django import forms
from django.forms import inlineformset_factory
from estudiantes.models import Estudiante, ApoderadoTitular
from app.models import (
    BitacoraEstudiante, PromedioSemanalHistorico, PromedioMensualHistorico,
    AnamnesisEstudiante, Familiar, Pai, EquipoResponsablePai, Docentes,
    Familia, EstrategiasDiversificadas, ApoyosEspecializados, HorarioApoyos,
    Firma
)
from .models import (
    ColumnasObjetivosAprendizaje, Paci, EquipoResponsablePaci, AulaRecursos, AulaRegular, PresentacionRepresentacion,
    MediosEjecucionExpresion, MultiplesMedios, Entorno, OrganizacionTiempo,
    GraduacionComplejidad, PriorizacionOA, Temporalizacion, EnriquecimientoCurriculum,
    ObjetivosAprendizaje, ColaboracionFamilia, CritEvaluacionPromocion, SeguimientoPaci,
    FirmaPaci
)


#_____________________________________________________________________________________________________________

# FORMULARIO PARA DE UN ESTUDIANTE
class EstudianteForm(forms.ModelForm):
    """
    Formulario para la creación y edición de estudiantes.
    """
    fecha_nacimiento = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'dd-mm-yyyy'}),
        label='Fecha de Nacimiento'
    )

    class Meta:
        model = Estudiante
        fields = ['nee', 'cursos', 'rut', 'nombres', 'apellido_paterno', 'apellido_materno', 'fecha_nacimiento', 'direccion', 'telefono', 'correo', 'region', 'comuna', 'etnia', 'comorbilidad']

    def clean_fecha_nacimiento(self):
        """
        Valida y convierte la fecha de nacimiento al formato correcto.
        """
        fecha_nacimiento = self.cleaned_data.get('fecha_nacimiento')
        try:
            # Convertir la fecha de 'dd-mm-yyyy' a un objeto de fecha
            fecha_nacimiento = datetime.strptime(fecha_nacimiento, '%d-%m-%Y').date()
        except ValueError:
            raise forms.ValidationError('Formato de fecha inválido. Use dd-mm-yyyy.')
        return fecha_nacimiento

    def clean_nombres(self):
        """
        Capitaliza el campo de nombres.
        """
        nombres = self.cleaned_data.get('nombres')
        return nombres.capitalize()

    def clean_apellido_paterno(self):
        """
        Capitaliza el campo de apellido paterno.
        """
        apellido_paterno = self.cleaned_data.get('apellido_paterno')
        return apellido_paterno.capitalize()

    def clean_apellido_materno(self):
        """
        Capitaliza el campo de apellido materno.
        """
        apellido_materno = self.cleaned_data.get('apellido_materno')
        return apellido_materno.capitalize()

    def clean_direccion(self):
        """
        Capitaliza el campo de dirección.
        """
        direccion = self.cleaned_data.get('direccion')
        return direccion.capitalize()

# FORM APODERADO TITULAR
class ApoderadoTitularForm(forms.ModelForm):
    """
    Formulario para la creación y edición de apoderados titulares.
    """
    fecha_nacimiento = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'dd-mm-yyyy'}),
        label='Fecha de Nacimiento'
    )

    class Meta:
        model = ApoderadoTitular
        fields = ['rut', 'etnia', 'fecha_nacimiento', 'nombres', 'apellido_paterno', 'apellido_materno', 'direccion', 'telefono', 'salud', 'renta', 'email', 'region', 'comuna']

    def clean_fecha_nacimiento(self):
        """
        Valida y convierte la fecha de nacimiento al formato correcto.
        """
        fecha_nacimiento = self.cleaned_data.get('fecha_nacimiento')
        try:
            # Convertir la fecha de 'dd-mm-yyyy' a un objeto de fecha
            fecha_nacimiento = datetime.strptime(fecha_nacimiento, '%d-%m-%Y').date()
        except ValueError:
            raise forms.ValidationError('Formato de fecha inválido. Use dd-mm-yyyy.')
        return fecha_nacimiento

    def clean_nombres(self):
        """
        Capitaliza el campo de nombres.
        """
        nombres = self.cleaned_data.get('nombres')
        return nombres.capitalize()

    def clean_apellido_paterno(self):
        """
        Capitaliza el campo de apellido paterno.
        """
        apellido_paterno = self.cleaned_data.get('apellido_paterno')
        return apellido_paterno.capitalize()

    def clean_apellido_materno(self):
        """
        Capitaliza el campo de apellido materno.
        """
        apellido_materno = self.cleaned_data.get('apellido_materno')
        return apellido_materno.capitalize()

    def clean_direccion(self):
        """
        Capitaliza el campo de dirección.
        """
        direccion = self.cleaned_data.get('direccion')
        return direccion.capitalize()
        
#_____________________________________________________________________________________________________________


#_____________________________________________________________________________________________________________

# FORMULARIO PARA REGISTRO DE BITÁCORA DE UN ESTUDIANTE
class BitacoraEstudianteForm(forms.ModelForm):
    class Meta:
        model = BitacoraEstudiante
        fields = ['estudiante', 'fecha', 'horas_estudiante', 'aula', 'asignatura', 'actividad', 'observaciones', 'nivelLogro']
        widgets = {
            'asignatura': forms.Select(attrs={'class': 'form-control'}),
            'nivelLogro': forms.RadioSelect(choices=[(True, 'Logrado'), (False, 'En Vías de Logro')], attrs={'class': 'form-check-input'}),
        }

#_____________________________________________________________________________________________________________

#FORMULARIO PARA AGREGAR UNA NUEVA SEMANA
class PromedioSemanalHistoricoForm(forms.ModelForm):
    class Meta:
        model = PromedioSemanalHistorico
        fields = ['inicio_semana', 'fin_semana']


#_____________________________________________________________________________________________________________
#FORMULARIO PARA AGREGAR UN NUEVO MES

class PromedioMensualHistoricoForm(forms.ModelForm):    
    class Meta:
        model = PromedioMensualHistorico
        fields = ['inicio_mes', 'fin_mes']

#_____________________________________________________________________________________________________________


class AnamnesisEstudianteForm(forms.ModelForm):
    class Meta:
        model = AnamnesisEstudiante
        fields = [
            'pais_natal', 'sexo', 'lengua', 
            'alumno_trabajador', 'entrevistador', 'fecha_entrevista', 
            'definicion_problema', 'pediatria', 'kinesiologia', 'genetico', 
            'fonoaudiologia', 'neurologia', 'psicologia', 'psiquiatria', 
            'psicopedagogia', 'terapia_ocupacional', 'otro', 'perdida_auditiva', 
            'perdida_visual', 'motor', 'paraplejia', 'trastorno_conductual', 
            'otros', 'observaciones'
        ]
        widgets = {
            'estudiante': forms.TextInput(attrs={'class': 'w-full bg-transparent focus:outline-none text-sm rounded-xl', 'readonly': 'readonly'}),
            'curso_actual': forms.TextInput(attrs={'class': 'w-full bg-transparent focus:outline-none text-sm rounded-xl', 'readonly': 'readonly'}),
            'edad': forms.NumberInput(attrs={
                'class': 'w-full bg-transparent focus:outline-none text-sm rounded-xl',
                'min': 15,
                'max': 99,
                'value': 15  # Valor inicial
            }),
            'pais_natal': forms.Select(attrs={'class': 'px-2 py-2 w-full bg-transparent focus:outline-none text-sm rounded-xl'}),
            'sexo': forms.RadioSelect(attrs={'class': 'mr-2 text-sm rounded-xl'}),
            'lengua': forms.Select(attrs={'class': 'py-2 px-2 w-full bg-transparent focus:outline-none text-sm rounded-xl'}),
            'alumno_trabajador': forms.RadioSelect(choices=[(True, 'Sí'), (False, 'No')], attrs={'class': 'mr-2 text-sm rounded-xl'}),
            'fecha_entrevista': forms.DateInput(attrs={'class': 'w-full bg-transparent focus:outline-none text-sm rounded-xl', 'type': 'date'}),
            'definicion_problema': forms.Textarea(attrs={'class': 'w-full bg-transparent focus:outline-none text-sm rounded-xl'}),
            'otros': forms.Textarea(attrs={'class': 'h-16 w-full px-3 py-2 bg-transparent focus:outline-none text-sm rounded-xl'}),
            'observaciones': forms.Textarea(attrs={'class': 'w-full bg-transparent focus:outline-none text-sm rounded-xl'}),
        }

FamiliarFormSet = inlineformset_factory(
    AnamnesisEstudiante, Familiar, 
    form=forms.ModelForm, 
    fields=['nombre', 'parentesco', 'edad', 'escolaridad', 'ocupacion_actual'], 
    widgets={
        'nombre': forms.TextInput(attrs={'class': 'w-full bg-transparent focus:outline-none text-sm rounded-xl'}),
        'parentesco': forms.Select(attrs={'class': 'w-full py-2 px-2 bg-transparent focus:outline-none text-sm rounded-xl'}),
        'edad': forms.NumberInput(attrs={
            'class': 'w-full bg-transparent focus:outline-none text-sm rounded-xl',
            'min': 15,
            'max': 99,
            'value': 15  # Valor inicial
        }),
        'escolaridad': forms.TextInput(attrs={'class': 'w-full bg-transparent focus:outline-none text-sm rounded-xl'}),
        'ocupacion_actual': forms.TextInput(attrs={'class': 'w-full bg-transparent focus:outline-none text-sm rounded-xl'}),
    },
    extra=1, can_delete=True
)

#_____________________________________________________________________________________________________________
#FORMULARIO PARA REGISTRO DE PAI DE UN ESTUDIANTE

class PaiEstudianteForm(forms.ModelForm):
    class Meta:
        model = Pai
        fields = ['sexo', 'fecha_elaboracion', 'rbd', 'nombre_establecimiento', 'region', 'comuna', 'coordinador_pie']
        widgets = {
            'estudiante': forms.TextInput(attrs={'class': 'w-full bg-transparent focus:outline-none text-sm rounded-xl', 'readonly': 'readonly'}),
            'curso_actual': forms.TextInput(attrs={'class': 'w-full bg-transparent focus:outline-none text-sm rounded-xl', 'readonly': 'readonly'}),
            'edad': forms.NumberInput(attrs={
                'class': 'w-full bg-transparent focus:outline-none text-sm rounded-xl',
                'min': 15,
                'max': 99,
                'value': 15  # Valor inicial
            }),
        }

    def clean_nombre_establecimiento(self):
        nombre_establecimiento = self.cleaned_data.get('nombre_establecimiento')
        return nombre_establecimiento.capitalize()

    def clean_rbd(self):
        rbd = self.cleaned_data.get('rbd')
        return rbd.capitalize()

# Formsets para los modelos relacionados
class EquipoResponsablePaiForm(forms.ModelForm):
    class Meta:
        model = EquipoResponsablePai
        fields = ['nombre_profesional', 'cargo']
        widgets = {
            'nombre_profesional': forms.TextInput(attrs={'class': 'w-full bg-transparent focus:outline-none text-sm rounded-xl'}),
            'cargo': forms.Select(attrs={'class': 'w-full py-2 px-3 bg-transparent focus:outline-none text-sm rounded-xl'}),
        }

EquipoResponsablePaiFormSet = inlineformset_factory(
    Pai, EquipoResponsablePai,
    form=EquipoResponsablePaiForm,
    extra=1, can_delete=True
)

class DocentesForm(forms.ModelForm):
    class Meta:
        model = Docentes
        fields = ['nombre', 'profesion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'w-full py-2 px-3 bg-transparent focus:outline-none text-sm rounded-xl'}),
            'profesion': forms.Select(attrs={'class': 'w-full py-2 px-3 bg-transparent focus:outline-none text-sm rounded-xl'}),
        }

DocentesFormSet = inlineformset_factory(
    Pai, Docentes,
    form=DocentesForm,
    extra=1, can_delete=True
)

class FamiliaForm(forms.ModelForm):
    class Meta:
        model = Familia
        fields = ['nombres', 'parentesco']
        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'w-full py-2 px-3 bg-transparent focus:outline-none text-sm rounded-xl'}),
            'parentesco': forms.Select(attrs={'class': 'w-full py-2 px-3 bg-transparent focus:outline-none text-sm rounded-xl'}),
        }

FamiliaFormSet = inlineformset_factory(
    Pai, Familia,
    form=FamiliaForm,
    extra=1, can_delete=True
)

class EstrategiasDiversificadasForm(forms.ModelForm):
    class Meta:
        model = EstrategiasDiversificadas
        fields = ['criterio', 'estrategias', 'metodo']
        widgets = {
            'criterio': forms.Textarea(attrs={'class': 'w-full px-3 py-2 h-40 bg-transparent focus:outline-none text-sm rounded-xl'}),
            'estrategias': forms.Textarea(attrs={'class': 'w-full px-3 py-2 h-40 bg-transparent focus:outline-none text-sm rounded-xl'}),
            'metodo': forms.Textarea(attrs={'class': 'w-full h-40 px-3 py-2 bg-transparent focus:outline-none text-sm rounded-xl'}),
        }

EstrategiasDiversificadasFormSet = inlineformset_factory(
    Pai, EstrategiasDiversificadas,
    form=EstrategiasDiversificadasForm,
    extra=1, can_delete=True
)

class ApoyosEspecializadosForm(forms.ModelForm):
    class Meta:
        model = ApoyosEspecializados
        fields = ['descripcion', 'contexto']
        widgets = {
            'descripcion': forms.Textarea(attrs={'class': 'w-full px-3 py-2 h-32 bg-transparent focus:outline-none text-sm rounded-xl'}),
            'contexto': forms.Textarea(attrs={'class': 'w-full px-3 py-2 h-32 bg-transparent focus:outline-none text-sm rounded-xl'}),
        }

ApoyosEspecializadosFormSet = inlineformset_factory(
    Pai, ApoyosEspecializados,
    form=ApoyosEspecializadosForm,
    extra=1, can_delete=True
)

class HorarioApoyosForm(forms.ModelForm):
    class Meta:
        model = HorarioApoyos
        fields = ['dia', 'horario', 'profesional', 'contexto']
        widgets = {
            'dia': forms.TextInput(attrs={'class': 'w-full bg-transparent focus:outline-none text-sm rounded-xl'}),
            'horario': forms.TextInput(attrs={'class': 'w-full bg-transparent focus:outline-none text-sm rounded-xl'}),
            'profesional': forms.Select(attrs={'class': 'w-full py-2 px-3 bg-transparent focus:outline-none text-sm rounded-xl'}),
            'contexto': forms.TextInput(attrs={'class': 'w-full bg-transparent focus:outline-none text-sm rounded-xl'}),
        }

HorarioApoyosFormSet = inlineformset_factory(
    Pai, HorarioApoyos,
    form=HorarioApoyosForm,
    extra=1, can_delete=True
)

class FirmaForm(forms.ModelForm):
    class Meta:
        model = Firma
        fields = ['nombre', 'cargo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'w-full bg-transparent focus:outline-none text-sm rounded-xl'}),
            'cargo': forms.TextInput(attrs={'class': 'w-full bg-transparent focus:outline-none text-sm rounded-xl'}),
        }

FirmaFormSet = inlineformset_factory(
    Pai, Firma,
    form=FirmaForm,
    extra=1, can_delete=True
)


#_____________________________________________________________________________________________________________
# FORMULARIO PARA REGISTRO DE PACI DE UN ESTUDIANTE
class PaciForm(forms.ModelForm):
    class Meta:
        model = Paci
        fields = ['sexo', 'fecha_elaboracion', 'fecha_revision', 'duracion', 'antecedentes_salud', \
                  'antecedentes_escolares', 'antecedentes_familiares', 'expectativas', 'apoyos',\
                  'rbd', 'nombre_establecimiento', 'region', 'comuna', 'coordinador_pie', 'jefe_utp']
        widgets = {
            'estudiante': forms.Select(attrs={'class': 'w-full bg-transparent focus:outline-none text-sm rounded-xl'}),
            'curso': forms.Select(attrs={'class': 'w-full bg-transparent focus:outline-none text-sm rounded-xl'}),
            'sexo': forms.Select(attrs={'class': 'w-full bg-transparent focus:outline-none text-sm rounded-xl'}),
            'edad': forms.NumberInput(attrs={'class': 'w-full bg-transparent focus:outline-none text-sm rounded-xl'}),
            'fecha_elaboracion': forms.DateInput(attrs={'class': 'w-full bg-transparent focus:outline-none text-sm rounded-xl', 'type': 'date'}),
            'fecha_revision': forms.DateInput(attrs={'class': 'w-full bg-transparent focus:outline-none text-sm rounded-xl', 'type': 'date'}),
            'duracion': forms.NumberInput(attrs={'class': 'w-full bg-transparent focus:outline-none text-sm rounded-xl'}),
            'rbd': forms.TextInput(attrs={'class': 'w-full bg-transparent focus:outline-none text-sm rounded-xl'}),
            'nombre_establecimiento': forms.TextInput(attrs={'class': 'w-full bg-transparent focus:outline-none text-sm rounded-xl'}),
            'comuna': forms.Select(attrs={'class': 'w-full bg-transparent focus:outline-none text-sm rounded-xl'}),
            'coordinador_pie': forms.Select(attrs={'class': 'w-full bg-transparent focus:outline-none text-sm rounded-xl'}),
            'jefe_utp': forms.TextInput(attrs={'class': 'w-full bg-transparent focus:outline-none text-sm rounded-xl'}),
        }

    def clean_nombre_establecimiento(self):
        nombre_establecimiento = self.cleaned_data.get('nombre_establecimiento')
        return nombre_establecimiento.capitalize()

    def clean_rbd(self):
        rbd = self.cleaned_data.get('rbd')
        return rbd.capitalize()

# Formsets para los modelos relacionados
EquipoResponsablePaciFormSet = inlineformset_factory(
    Paci, EquipoResponsablePaci,
    fields=['nombre', 'profesion', 'funcion', 'n_registro'],
    widgets={
        'nombre': forms.TextInput(attrs={'class': 'w-full bg-transparent focus:outline-none text-sm rounded-xl'}),
        'profesion': forms.Select(attrs={'class': 'w-full px-3 py-2 bg-transparent focus:outline-none text-sm rounded-xl'}),
        'funcion': forms.Textarea(attrs={'class': 'w-full px-3 py-2 bg-transparent focus:outline-none text-sm rounded-xl'}),
        'n_registro': forms.TextInput(attrs={'class': 'w-full px-3 py-2 bg-transparent focus:outline-none text-sm rounded-xl'}),
    },
    extra=1, can_delete=True
)

AulaRecursosFormSet = inlineformset_factory(
    Paci, AulaRecursos,
    fields=['aula_de_recursos'],
    widgets={
        'aula_de_recursos': forms.Textarea(attrs={'class': 'w-full h-20 px-3 py-2 bg-transparent focus:outline-none text-sm rounded-xl'}),
    },
    extra=1, can_delete=True
)

AulaRegularFormSet = inlineformset_factory(
    Paci, AulaRegular,
    fields=['aula_regular'],
    widgets={
        'aula_regular': forms.Textarea(attrs={'class': 'w-full px-3 py-2 h-20 bg-transparent focus:outline-none text-sm rounded-xl'}),
    },
    extra=1, can_delete=True
)

PresentacionRepresentacionFormSet = inlineformset_factory(
    Paci, PresentacionRepresentacion,
    fields=['presentacion_representacion'],
    widgets={
        'presentacion_representacion': forms.Textarea(attrs={'class': 'w-full px-3 py-2 h-16 bg-transparent focus:outline-none text-sm rounded-xl'}),
    },
    extra=1, can_delete=True
)

MediosEjecucionExpresionFormSet = inlineformset_factory(
    Paci, MediosEjecucionExpresion,
    fields=['medios_ejecucion_expresion'],
    widgets={
        'medios_ejecucion_expresion': forms.Textarea(attrs={'class': 'w-full px-3 py-2 h-16 bg-transparent focus:outline-none text-sm rounded-xl'}),
    },
    extra=1, can_delete=True
)

MultiplesMediosFormSet = inlineformset_factory(
    Paci, MultiplesMedios,
    fields=['multiples_medios'],
    widgets={
        'multiples_medios': forms.Textarea(attrs={'class': 'w-full px-3 py-2 h-16 bg-transparent focus:outline-none text-sm rounded-xl'}),
    },
    extra=1, can_delete=True
)

EntornoFormSet = inlineformset_factory(
    Paci, Entorno,
    fields=['entorno'],
    widgets={
        'entorno': forms.Textarea(attrs={'class': 'w-full px-3 py-2 h-16 bg-transparent focus:outline-none text-sm rounded-xl'}),
    },
    extra=1, can_delete=True
)

OrganizacionTiempoFormSet = inlineformset_factory(
    Paci, OrganizacionTiempo,
    fields=['organizacion_tiempo'],
    widgets={
        'organizacion_tiempo': forms.Textarea(attrs={'class': 'w-full px-3 py-2 h-16 bg-transparent focus:outline-none text-sm rounded-xl'}),
    },
    extra=1, can_delete=True
)

GraduacionComplejidadFormSet = inlineformset_factory(
    Paci, GraduacionComplejidad,
    fields=['graduacion_complejidad'],
    widgets={
        'graduacion_complejidad': forms.Textarea(attrs={'class': 'w-full px-3 py-2 h-16 bg-transparent focus:outline-none text-sm rounded-xl'}),
    },
    extra=1, can_delete=True
)

PriorizacionOAFormSet = inlineformset_factory(
    Paci, PriorizacionOA,
    fields=['priorizacion_oa'],
    widgets={
        'priorizacion_oa': forms.Textarea(attrs={'class': 'w-full px-3 py-2 h-16 bg-transparent focus:outline-none text-sm rounded-xl'}),
    },
    extra=1, can_delete=True
)

TemporalizacionFormSet = inlineformset_factory(
    Paci, Temporalizacion,
    fields=['temporalizacion'],
    widgets={
        'temporalizacion': forms.Textarea(attrs={'class': 'w-full px-3 py-2 h-16 bg-transparent focus:outline-none text-sm rounded-xl'}),
    },
    extra=1, can_delete=True
)

EnriquecimientoCurriculumFormSet = inlineformset_factory(
    Paci, EnriquecimientoCurriculum,
    fields=['enriquecimiento_curriculum'],
    widgets={
        'enriquecimiento_curriculum': forms.Textarea(attrs={'class': 'w-full px-3 py-2 h-16 bg-transparent focus:outline-none text-sm rounded-xl'}),
    },
    extra=1, can_delete=True
)

ObjetivosAprendizajeFormSet = inlineformset_factory(
    Paci, ObjetivosAprendizaje,
    fields=['nivel_ensenanza', 'curso', 'asignatura_o_nucleo', 'eje_o_ambito', 'espacio_educativo'],
    widgets={
        'nivel_ensenanza': forms.Select(attrs={'class': 'w-full px-3 py-2 bg-transparent focus:outline-none text-sm rounded-xl'}),
        'curso': forms.TextInput(attrs={'class': 'w-full bg-transparent focus:outline-none text-sm rounded-xl'}),
        'asignatura_o_nucleo': forms.TextInput(attrs={'class': 'w-full bg-transparent focus:outline-none text-sm rounded-xl'}),
        'eje_o_ambito': forms.TextInput(attrs={'class': 'w-full bg-transparent focus:outline-none text-sm rounded-xl'}),
        'espacio_educativo': forms.TextInput(attrs={'class': 'w-full bg-transparent focus:outline-none text-sm rounded-xl'}),
    },
    extra=1, can_delete=True
)

ColumnasObjetivosAprendizajeFormSet = inlineformset_factory(
    Paci, ColumnasObjetivosAprendizaje,
    fields=['codigo', 'objetivos_aprendizaje', 'adaptacion_de_oa', 'estrategias_metodologicas', 'evaluacion_de_oa'],
    widgets={
        'codigo': forms.TextInput(attrs={'class': 'w-full bg-transparent focus:outline-none text-sm rounded-xl'}),
        'objetivos_aprendizaje': forms.Textarea(attrs={'class': 'w-full px-3 py-2 bg-transparent focus:outline-none text-sm rounded-xl'}),
        'adaptacion_de_oa': forms.Textarea(attrs={'class': 'w-full px-3 py-2 bg-transparent focus:outline-none text-sm rounded-xl'}),
        'estrategias_metodologicas': forms.Textarea(attrs={'class': 'w-full px-3 py-2 bg-transparent focus:outline-none text-sm rounded-xl'}),
        'evaluacion_de_oa': forms.Textarea(attrs={'class': 'w-full px-3 py-2 bg-transparent focus:outline-none text-sm rounded-xl'}),
    },
    extra=1, can_delete=True
)

ColaboracionFamiliaFormSet = inlineformset_factory(
    Paci, ColaboracionFamilia,
    fields=['aspectos_familia'],
    widgets={
        'aspectos_familia': forms.Textarea(attrs={'class': 'w-full px-3 py-2 h-16 bg-transparent focus:outline-none text-sm rounded-xl'}),
    },
    extra=1, can_delete=True
)

CritEvaluacionPromocionFormSet = inlineformset_factory(
    Paci, CritEvaluacionPromocion,
    fields=['criterios'],
    widgets={
        'criterios': forms.Textarea(attrs={'class': 'w-full px-3 py-2 h-16 bg-transparent focus:outline-none text-sm rounded-xl'}),
    },
    extra=1, can_delete=True
)

SeguimientoPaciFormSet = inlineformset_factory(
    Paci, SeguimientoPaci,
    fields=['seguimiento'],
    widgets={
        'seguimiento': forms.Textarea(attrs={'class': 'w-full px-3 py-2 h-16 bg-transparent focus:outline-none text-sm rounded-xl'}),
    },
    extra=1, can_delete=True
)

FirmaPaciFormSet = inlineformset_factory(
    Paci, FirmaPaci,
    fields=['nombre', 'cargo'],
    widgets={
        'nombre': forms.TextInput(attrs={'class': 'w-full bg-transparent focus:outline-none text-sm rounded-xl'}),
        'cargo': forms.TextInput(attrs={'class': 'w-full bg-transparent focus:outline-none text-sm rounded-xl'}),
    },
    extra=1, can_delete=True
)