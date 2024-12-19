"""
Autores:
Raúl Córdova Vicencio
Francisca Olavarría Pavez
Carlos Olivero Bruno

Fecha: 01 diciembre 2024

Descripción:
Este módulo define los modelos de datos para la aplicación de gestión de estudiantes. Incluye modelos para áreas académicas, cursos, estudiantes, apoderados, bitácoras, promedios y formularios de evaluación. Cada modelo está diseñado para representar una entidad específica en el sistema y contiene campos relevantes, métodos y validaciones para garantizar la integridad de los datos.

Modelos:
- AreaAcademica: Representa un área académica específica.
- Curso: Representa un curso dentro de un área académica.
- Persona: Clase abstracta que define atributos comunes para personas.
- Estudiante: Hereda de Persona y añade atributos específicos para estudiantes.
- ApoderadoTitular: Hereda de Persona y añade atributos específicos para apoderados.
- Asignatura: Representa una asignatura específica.
- BitacoraEstudiante: Registra actividades y observaciones diarias de los estudiantes.
- PromedioDia: Calcula y almacena el promedio diario de logros de un estudiante.
- PromedioSemanalHistorico: Calcula y almacena el promedio semanal histórico de logros de un estudiante.
- PromedioMensualHistorico: Calcula y almacena el promedio mensual histórico de logros de un estudiante.
- AnamnesisEstudiante: Registra información detallada sobre el estudiante y su entorno.
- Familiar: Registra información sobre los familiares del estudiante.
- Pai: Registra el Plan de Apoyo Individual (PAI) de un estudiante.
- EquipoResponsablePai: Registra los profesionales responsables del PAI.
- Docentes: Registra los docentes integradores y familiares involucrados en el PAI.
- EstrategiasDiversificadas: Registra estrategias diversificadas en el aula para el PAI.
- ApoyosEspecializados: Registra apoyos especializados para el PAI.
- HorarioApoyos: Registra el horario de los apoyos especializados para el PAI.
- Firma: Registra las firmas del equipo responsable del PAI.
- Paci: Registra el Plan de Apoyo Curricular Individual (PACI) de un estudiante.
- EquipoResponsablePaci: Registra los profesionales responsables del PACI.
- AulaRecursos: Registra recursos y modalidades de apoyo en el aula para el PACI.
- AulaRegular: Registra modalidades de apoyo en el aula regular para el PACI.
- PresentacionRepresentacion: Registra adecuaciones de acceso en la presentación y representación de la información para el PACI.
- MediosEjecucionExpresion: Registra adecuaciones de acceso en los medios de ejecución y expresión para el PACI.
- MultiplesMedios: Registra múltiples medios de participación y compromiso para el PACI.
- Entorno: Registra adecuaciones en el entorno para el PACI.
- OrganizacionTiempo: Registra la organización del tiempo y el horario para el PACI.
- GraduacionComplejidad: Registra la graduación del nivel de complejidad para el PACI.
- PriorizacionOA: Registra la priorización de objetivos de aprendizaje (OA) y contenidos para el PACI.
- Temporalizacion: Registra la temporalización de los objetivos de aprendizaje para el PACI.
- EnriquecimientoCurriculum: Registra el enriquecimiento del currículo para el PACI.
- ObjetivosAprendizaje: Registra los objetivos de aprendizaje para el PACI.
- ColumnasObjetivosAprendizaje: Registra columnas de objetivos de aprendizaje para el PACI.
- ColaboracionFamilia: Registra la colaboración de la familia en el PACI.
- CritEvaluacionPromocion: Registra los criterios de evaluación y promoción para el PACI.
- SeguimientoPaci: Registra el seguimiento del PACI.
- FirmaPaci: Registra las firmas del equipo responsable del PACI.

Señales:
- estudiante_pre_save: Señal pre_save para estandarizar el formato de las cadenas en el modelo Estudiante.

Validadores:
- validate_edad: Validador para asegurar que la edad esté entre 15 y 99 años.
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, EmailValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from accounts.models import Profile
from localidad.models import Comuna, Region
from .opciones import opciones_ascendencia, opciones_salud, opciones_nee, opciones_aula\
    , opciones_pais, opciones_sexo, opciones_lengua, opciones_parentesco, opciones_docente\
    , opciones_profesional, opciones_educacion

# MODELO AREA ACADÉMICA
class AreaAcademica(models.Model):
    nombre = models.CharField(max_length=150, verbose_name='Nombre del Área Académica')

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Área Académica'
        verbose_name_plural = 'Áreas Académicas'

# MODELO PARA REGISTRAR LOS CURSOS
class Curso(models.Model):
    nombre = models.CharField(max_length=150, verbose_name='Nombre del Curso')
    area_academica = models.ForeignKey(AreaAcademica, on_delete=models.CASCADE, verbose_name='Área Académica')

    def __str__(self):
        return self.nombre 

    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'

# CLASE ABSTRACTA PARA PERSONA
class Persona(models.Model):
    rut = models.CharField(max_length=12, unique=True, verbose_name="Rut")
    nombres = models.CharField(max_length=100, verbose_name="Nombres")
    apellido_paterno = models.CharField(max_length=100, verbose_name="Apellido Paterno")
    apellido_materno = models.CharField(max_length=100, verbose_name="Apellido Materno")
    fecha_nacimiento = models.DateField(verbose_name="Fecha de Nacimiento", blank=True, null=True)
    direccion = models.CharField(max_length=100, verbose_name='Dirección')
    telefono = models.CharField(max_length=9, verbose_name='Teléfono')

    class Meta:
        abstract = True  # Hace que este modelo sea abstracto y no se cree una tabla en la base de datos
    
# MODELO ESTUDIANTE
class Estudiante(Persona):  # Heredamos de la clase Persona (Modelo Abstracto)
    nee = models.CharField(max_length=100, choices=opciones_nee, verbose_name='Necesidades Educativas')
    cursos = models.ForeignKey(Curso, on_delete=models.CASCADE, verbose_name='Curso')
    correo = models.EmailField(validators=[EmailValidator()], verbose_name='Correo Electrónico')
    region = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name='Region', blank=True, null=True)
    comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE, verbose_name='Comuna', blank=True, null=True)
    etnia = models.CharField(max_length=100, default='No Posee', choices=opciones_ascendencia, verbose_name='Ascendencia')
    comorbilidad = models.TextField(verbose_name='Comorbilidad')

    def __str__(self):
        return f'{self.nombres} {self.apellido_paterno} {self.apellido_materno}'
    
    class Meta:
        verbose_name = 'Estudiante'
        verbose_name_plural = 'Estudiantes'

# Definición de la señal pre_save para estandarizar el formato de las cadenas
@receiver(pre_save, sender=Estudiante)
def estudiante_pre_save(sender, instance, *args, **kwargs):
    # Asegura que los nombres y apellidos estén en formato título (primera letra en mayúscula)
    instance.nombres = instance.nombres.title()
    instance.apellido_paterno = instance.apellido_paterno.title()
    instance.apellido_materno = instance.apellido_materno.title()
    # Asegura que la dirección esté en formato título (primera letra en mayúscula en cada palabra)
    instance.direccion = instance.direccion.title()
    # Asegura que la comorbilidad esté en minúsculas
    instance.comorbilidad = instance.comorbilidad.lower()

# MODELO APODERADO TITULAR
class ApoderadoTitular(Persona):
    estudiante = models.OneToOneField(Estudiante, on_delete=models.CASCADE, verbose_name='Estudiante', blank=True, null=True)
    email = models.EmailField(validators=[EmailValidator()], verbose_name='Email')
    region = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name='Region', blank=True, null=True)
    comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE, verbose_name='Comuna', blank=True, null=True)
    etnia = models.CharField(max_length=100, default='No Posee', choices=opciones_ascendencia, verbose_name='Ascendencia', blank=True, null=True)
    salud = models.CharField(max_length=100, default='Seleccione', choices=opciones_salud, verbose_name='Salud', blank=True, null=True)
    renta = models.PositiveIntegerField(verbose_name='Renta', blank=True, null=True)

    def __str__(self):
        return f'{self.nombres} {self.apellido_paterno} {self.apellido_materno}'

    class Meta:
        verbose_name = 'Apoderado Titular'
        verbose_name_plural = 'Apoderados Titulares'


        

# MODELO ASIGNATURA
class Asignatura(models.Model):
    asignatura = models.CharField(max_length=100, verbose_name='Asignatura:')

    def __str__(self):
        return self.asignatura

# MODELO BITÁCORA ESTUDIANTE
class BitacoraEstudiante(models.Model):
    profesional = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Profesional:', related_name='bitácoras_profesional')
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, verbose_name='Estudiante:', related_name='bitácoras_estudiante')
    fecha = models.DateField(verbose_name='Fecha:', default=timezone.now)
    aula = models.CharField(max_length=100, choices=opciones_aula, verbose_name='Aula:')
    horas_estudiante = models.PositiveIntegerField(verbose_name='Horas Estudiante:', validators=[MinValueValidator(1), MaxValueValidator(10)])
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE, verbose_name='Asignatura:', related_name='bitácoras_asignatura')
    actividad = models.TextField(verbose_name='Actividad:', blank=True)
    observaciones = models.TextField(verbose_name='Observaciones:', blank=True)
    nivelLogro = models.BooleanField(default=False, verbose_name='Nivel de Logro (True = Logrado, False = En Vías de Logro)')

    def __str__(self):
        return f'{self.estudiante} - {self.fecha}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.actualizar_promedios(self.fecha)

    def actualizar_promedios(self, fecha):
        # Actualiza el promedio diario
        promedio_dia, created = PromedioDia.objects.get_or_create(estudiante=self.estudiante, bitacora=self)
        promedio_dia.save()
        
        # Actualiza el promedio semanal histórico
        inicio_semana = fecha - timedelta(days=fecha.weekday())
        fin_semana = inicio_semana + timedelta(days=4)
        inicio_mes = fecha.replace(day=1)
        fin_mes = (inicio_mes + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        inicio_semana = max(inicio_semana, inicio_mes)
        fin_semana = min(fin_semana, fin_mes)
        promedio_semanal_historico, created = PromedioSemanalHistorico.objects.get_or_create(
            estudiante=self.estudiante,
            inicio_semana=inicio_semana,
            fin_semana=fin_semana
        )
        promedio_semanal_historico.promedio_semana = promedio_semanal_historico.calcular_promedio_semana()
        promedio_semanal_historico.save()
        
        # Actualiza el promedio mensual histórico
        promedio_mensual_historico, created = PromedioMensualHistorico.objects.get_or_create(
            estudiante=self.estudiante,
            inicio_mes=inicio_mes,
            fin_mes=fin_mes
        )
        promedio_mensual_historico.promedio_mes = promedio_mensual_historico.calcular_promedio_mes()
        promedio_mensual_historico.save()


#____________________________________________________________________________________________________________________________________
# MODELO PROMEDIO DIA
class PromedioDia(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, verbose_name='Estudiante')
    bitacora = models.OneToOneField(BitacoraEstudiante, on_delete=models.CASCADE, verbose_name='Bitácora')
    total_dia = models.FloatField(verbose_name='Total del Día (%)', default=0.0)

    # Calcula el total del día basado en las bitácoras del estudiante para la fecha específica
    def calcular_total_dia(self):
        bitacoras = BitacoraEstudiante.objects.filter(estudiante=self.bitacora.estudiante, fecha=self.bitacora.fecha)
        total = bitacoras.count()
        logrados = bitacoras.filter(nivelLogro=True).count()
        vias_logro = total - logrados
        return round(((logrados * 20 + vias_logro * 10) / (total * 20)) * 100, 1) if total > 0 else 0

    # Sobrescribe el método save para calcular y guardar el total del día
    def save(self, *args, **kwargs):
        self.total_dia = self.calcular_total_dia()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.bitacora.estudiante} - {self.bitacora.fecha} - {self.total_dia:.1f}%'


#____________________________________________________________________________________________________________________________________
# MODELO PROMEDIO SEMANAL HISTÓRICO
class PromedioSemanalHistorico(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, verbose_name='Estudiante')
    inicio_semana = models.DateField(verbose_name='Inicio de la Semana')
    fin_semana = models.DateField(verbose_name='Fin de la Semana')
    promedio_semana = models.FloatField(verbose_name='Promedio de la Semana (%)', default=0.0)

    def calcular_promedio_semana(self):
        bitacoras = BitacoraEstudiante.objects.filter(estudiante=self.estudiante, fecha__range=[self.inicio_semana, self.fin_semana])
        total_logrado = sum(20 if b.nivelLogro else 10 for b in bitacoras)
        total_bitacoras = bitacoras.count()
        return round((total_logrado / (total_bitacoras * 20)) * 100, 2) if total_bitacoras > 0 else 0

    def save(self, *args, **kwargs):
        self.promedio_semana = self.calcular_promedio_semana()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.estudiante} - {self.inicio_semana} to {self.fin_semana}'
#____________________________________________________________________________________________________________________________________
# MODELO PROMEDIO MENSUAL HISTÓRICO
class PromedioMensualHistorico(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, verbose_name='Estudiante')
    inicio_mes = models.DateField(verbose_name='Inicio del Mes')
    fin_mes = models.DateField(verbose_name='Fin del Mes')
    promedio_mes = models.FloatField(verbose_name='Promedio del Mes (%)', default=0.0)

    def calcular_promedio_mes(self):
        bitacoras = BitacoraEstudiante.objects.filter(estudiante=self.estudiante, fecha__range=[self.inicio_mes, self.fin_mes])
        total_logrado = sum(20 if b.nivelLogro else 10 for b in bitacoras)
        total_bitacoras = bitacoras.count()
        return round((total_logrado / (total_bitacoras * 20)) * 100, 2) if total_bitacoras > 0 else 0

    def save(self, *args, **kwargs):
        self.promedio_mes = self.calcular_promedio_mes()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.estudiante} - {self.inicio_mes} to {self.fin_mes}'

#____________________________________________________________________________________________________________________________________
#VALIDADOR DE LA EDAD
def validate_edad(value):
    if value < 15 or value > 99:
        raise ValidationError("La edad debe estar entre 15 y 99 años.")
    
# MODELO PARA REGISTRAR UN ANAMNESIS DE UN ESTUDIANTE
class AnamnesisEstudiante(models.Model):

    # 1. IDENTIFICACIÓN DEL ESTUDIANTE
    estudiante = models.OneToOneField(Estudiante, on_delete=models.CASCADE, verbose_name='Estudiante')
    curso_actual = models.ForeignKey(Curso, on_delete=models.CASCADE, verbose_name='Curso Actual')
    edad = models.PositiveIntegerField(verbose_name='Edad')
    pais_natal = models.CharField(max_length=150, choices=opciones_pais, verbose_name='País Natal', blank=True, null=True, default='Seleccione País')
    sexo = models.CharField(max_length=150, choices=opciones_sexo, verbose_name='Sexo', blank=True, null=True, default='Seleccione Sexo')
    lengua = models.CharField(max_length=150, choices=opciones_lengua, verbose_name='Lengua de uso', blank=True, null=True, default='Seleccione Lengua')
    alumno_trabajador = models.BooleanField(default=False, verbose_name='Alumno Trabajador (True = Sí, False = No)', blank=True, null=True)
    
    # 2. IDENTIFICACIÓN DEL ENTREVISTADOR
    entrevistador = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Entrevistador', blank=True, null=True)
    fecha_entrevista = models.DateField(verbose_name='Fecha de Entrevista', default=timezone.now, blank=True, null=True)

    # 3. DEFINICIÓN DEL PROBLEMA O SITUACIÓN QUE MOTIVA LA ENTREVISTA
    definicion_problema = models.TextField(verbose_name='Definición del Problema o Situación que Motiva la Entrevista', blank=True, null=True)

    # 4. ANTECEDENTES RELATIVOS AL DESARROLLO Y A LA SALUD DEL/LA ESTUDIANTE
    pediatria = models.BooleanField(default=False, verbose_name='Pediatría (True = Sí, False = No)', blank=True, null=True)
    kinesiologia = models.BooleanField(default=False, verbose_name='Kinesiología (True = Sí, False = No)', blank=True, null=True)
    genetico = models.BooleanField(default=False, verbose_name='Genético (True = Sí, False = No)', blank=True, null=True)
    fonoaudiologia = models.BooleanField(default=False, verbose_name='Fonoaudiología (True = Sí, False = No)', blank=True, null=True)
    neurologia = models.BooleanField(default=False, verbose_name='Neurología (True = Sí, False = No)', blank=True, null=True)
    psicologia = models.BooleanField(default=False, verbose_name='Psicología (True = Sí, False = No)', blank=True, null=True)
    psiquiatria = models.BooleanField(default=False, verbose_name='Psiquiatría (True = Sí, False = No)', blank=True, null=True)
    psicopedagogia = models.BooleanField(default=False, verbose_name='Psicopedagogía (True = Sí, False = No)', blank=True, null=True)
    terapia_ocupacional = models.BooleanField(default=False, verbose_name='Terapia Ocupacional (True = Sí, False = No)', blank=True, null=True)
    otro = models.BooleanField(default=False, verbose_name='Otro (True = Sí, False = No)', blank=True, null=True)

    # 5. SÍNTESIS DE LOS ANTECEDENTES DE SALUD, ESCOLARES Y SOCIALES DEL ESTUDIANTE
    perdida_auditiva = models.BooleanField(default=False, verbose_name='Pérdida Auditiva (True = Sí, False = No)', blank=True, null=True)
    perdida_visual = models.BooleanField(default=False, verbose_name='Pérdida Visual (True = Sí, False = No)', blank=True, null=True)
    motor = models.BooleanField(default=False, verbose_name='Motor (True = Sí, False = No)', blank=True, null=True)
    paraplejia = models.BooleanField(default=False, verbose_name='Paraplejia (True = Sí, False = No)', blank=True, null=True)
    trastorno_conductual = models.BooleanField(default=False, verbose_name='Trastorno Conductual (True = Sí, False = No)', blank=True, null=True)
    otros = models.TextField(verbose_name='Otros', blank=True, null=True)

    # 6. ANTECEDENTES FAMILIARES
    # AQUÍ SE RELACIONA UN MODELO DE MÁS ABAJO DE FAMILIARES
    
    # OBSERVACIONES
    observaciones = models.TextField(verbose_name='Observaciones', blank=True, null=True)
    
    def __str__(self):
        return f'{self.estudiante} - {self.fecha_entrevista}'

class Familiar(models.Model):
    anamnesis = models.ForeignKey(AnamnesisEstudiante, on_delete=models.CASCADE, related_name='familiares', verbose_name='Anamnesis')
    nombre = models.CharField(max_length=350, verbose_name='Nombre', blank=True, null=True)
    parentesco = models.CharField(max_length=150, choices=opciones_parentesco, verbose_name='Parentesco', blank=True, null=True)
    edad = models.PositiveIntegerField(verbose_name='Edad', validators=[validate_edad], blank=True, null=True)
    escolaridad = models.CharField(max_length=350, verbose_name='Escolaridad', blank=True, null=True)
    ocupacion_actual = models.CharField(max_length=350, verbose_name='Ocupación Actual', blank=True, null=True)

    def __str__(self):
        return f'{self.nombre} ({self.parentesco})'

#____________________________________________________________________________________________________________________________________

# MODELO PARA REGISTRAR INFORME EVALUACIÓN PAI DE UN ESTUDIANTE
class Pai(models.Model):

    # 1. IDENTIFICACIÓN DEL ESTUDIANTE
    estudiante = models.OneToOneField(Estudiante, on_delete=models.CASCADE, verbose_name='Estudiante')
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, verbose_name='Curso')
    edad = models.PositiveIntegerField(verbose_name='Edad', blank=True, null=True)
    sexo = models.CharField(max_length=150, choices=opciones_sexo, verbose_name='Sexo', blank=True, null=True)
    fecha_elaboracion = models.DateField(verbose_name='Fecha de Elaboración', blank=True, null=True)

    # 2. IDENTIFICACIÓN DEL ESTABLECIMIENTO
    rbd = models.CharField(max_length=150, verbose_name='RBD', blank=True, null=True)
    nombre_establecimiento = models.CharField(max_length=300, verbose_name='Nombre del Establecimiento', blank=True, null=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name='Region', blank=True, null=True)
    comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE, verbose_name='Comuna', blank=True, null=True)
    coordinador_pie = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Coordinador PIE', blank=True, null=True)

    def __str__(self):
        return f'{self.estudiante} - {self.fecha_elaboracion}'

# 3. EQUIPO RESPONSABLE
class EquipoResponsablePai(models.Model):
    pai = models.ForeignKey(Pai, on_delete=models.CASCADE, related_name='equipo_responsable', verbose_name='PAI')
    nombre_profesional = models.CharField(max_length=350, verbose_name='Nombre Profesional', blank=True, null=True)
    cargo = models.CharField(max_length=250, choices=opciones_profesional,  verbose_name='Cargo', blank=True, null=True)

    def __str__(self):
        return f'{self.nombre_profesional} - {self.cargo}'

# 4. DOCENTES INTEGRADORES Y FAMILIA
class Docentes(models.Model):
    pai = models.ForeignKey(Pai, on_delete=models.CASCADE, related_name='docentes', verbose_name='PAI')
    nombre = models.CharField(max_length=150, verbose_name='Nombre', blank=True, null=True)
    profesion = models.CharField(max_length=150, choices=opciones_docente, verbose_name='Profesión', blank=True, null=True)

    def __str__(self):
        return f'{self.nombre}'

# 4.1 FAMILIA
class Familia(models.Model):
    pai = models.ForeignKey(Pai, on_delete=models.CASCADE, related_name='familia', verbose_name='PAI')
    nombres = models.CharField(max_length=350, verbose_name='Nombres', blank=True, null=True)
    parentesco = models.CharField(max_length=150, choices=opciones_parentesco, verbose_name='Parentesco', blank=True, null=True)

    def __str__(self):
        return f'{self.nombres} {self.parentesco}'

# 5. ESTRATEGIAS DIVERSIFICADAS EN EL AULA
class EstrategiasDiversificadas(models.Model):
    pai = models.ForeignKey(Pai, on_delete=models.CASCADE, related_name='estrategias_diversificadas', verbose_name='PAI')
    criterio = models.TextField(verbose_name='Criterio', blank=True, null=True)
    estrategias = models.TextField(verbose_name='Estrategias para', blank=True, null=True)
    metodo = models.TextField(verbose_name='Método', blank=True, null=True)

    def __str__(self):
        return f'{self.criterio} - {self.estrategias} - {self.metodo}'

# 6. ORGANIZACIÓN DE LOS APOYOS ESPECIALIZADOS
class ApoyosEspecializados(models.Model):
    pai = models.ForeignKey(Pai, on_delete=models.CASCADE, related_name='apoyos_especializados', verbose_name='PAI')
    descripcion = models.TextField(verbose_name='Descripción', blank=True, null=True)
    contexto = models.TextField(verbose_name='Contexto', blank=True, null=True)

    def __str__(self):
        return f'{self.descripcion} - {self.contexto}'

# 7. HORARIO DE LOS APOYOS ESPECIALIZADOS
class HorarioApoyos(models.Model):
    pai = models.ForeignKey(Pai, on_delete=models.CASCADE, related_name='horario_apoyos', verbose_name='PAI')
    dia = models.CharField(max_length=150, verbose_name='Día', blank=True, null=True)
    horario = models.CharField(max_length=350, verbose_name='Horario', blank=True, null=True)
    profesional = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Profesional', blank=True, null=True)
    contexto = models.CharField(max_length=350, verbose_name='Contexto', blank=True, null=True)

    def __str__(self):
        return f'{self.dia} - {self.horario} - {self.profesional} - {self.contexto}'

# 8. FIRMA EQUIPO RESPONSABLE PAI
class Firma(models.Model):
    pai = models.ForeignKey(Pai, on_delete=models.CASCADE, related_name='firma', verbose_name='PAI')
    nombre = models.CharField(max_length=150, verbose_name='Nombre', blank=True, null=True)
    cargo = models.CharField(max_length=150, verbose_name='Cargo', blank=True, null=True)

    def __str__(self):
        return f'{self.nombre} - {self.cargo}'
    

#____________________________________________________________________________________________________________________________________

# MODELO PARA REGISTRAR UN FORMULARIO PACI DE UN ESTUDIANTE
class Paci(models.Model):

    # 1. IDENTIFICACIÓN DEL ESTUDIANTE
    estudiante = models.OneToOneField(Estudiante, on_delete=models.CASCADE, verbose_name='Estudiante')
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, verbose_name='Curso')
    sexo = models.CharField(max_length=150, choices=opciones_sexo, verbose_name='Sexo', blank=True, null=True)
    edad = models.PositiveIntegerField(verbose_name='Edad')
    fecha_elaboracion = models.DateField(verbose_name='Fecha de Elaboración', blank=True, null=True)
    fecha_revision = models.DateField(verbose_name='Fecha de Revisión', blank=True, null=True)
    duracion = models.PositiveIntegerField(verbose_name='Duración (en meses)', blank=True, null=True)
    antecedentes_salud = models.TextField(verbose_name='Antecedentes Relevantes de Salud', blank=True, null=True)
    antecedentes_escolares = models.TextField(verbose_name='Antecedentes Escolares', blank=True, null=True)
    antecedentes_familiares = models.TextField(verbose_name='Antecedentes Familiares (Con quien vive)', blank=True, null=True)
    expectativas = models.TextField(verbose_name='Expectativas, Sueños y Prioridades de la Familia', blank=True, null=True)
    apoyos = models.TextField(verbose_name='Apoyos que se requieren para lograrlo', blank=True, null=True)

    # 2. IDENTIFICACIÓN DEL ESTABLECIMIENTO
    rbd = models.CharField(max_length=150, verbose_name='RBD', blank=True, null=True)
    nombre_establecimiento = models.CharField(max_length=300, verbose_name='Nombre del Establecimiento', blank=True, null=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name='Region', blank=True, null=True)
    comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE, verbose_name='Comuna', blank=True, null=True)
    coordinador_pie = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Coordinador PIE', blank=True, null=True)
    jefe_utp = models.CharField(max_length=350, verbose_name='Jefe UTP', blank=True, null=True)

    def __str__(self):
        return f'{self.estudiante} - {self.fecha_elaboracion}'

# 3. EQUIPO RESPONSABLE
class EquipoResponsablePaci(models.Model):
    paci = models.ForeignKey(Paci, on_delete=models.CASCADE, verbose_name='PACI', related_name='equipo_responsable')
    nombre = models.CharField(max_length=350, verbose_name='Nombre', blank=True, null=True)
    profesion = models.CharField(max_length=150, choices=opciones_profesional, verbose_name='Profesión', blank=True, null=True)
    funcion = models.TextField(verbose_name='Función', blank=True, null=True)
    n_registro = models.CharField(max_length=150, verbose_name='N° Registro', blank=True, null=True)

    def __str__(self):
        return f'{self.nombre} - {self.profesion} - {self.funcion} - {self.n_registro}'

# 4. RECURSOS Y MODALIDAD DE APOYO
class AulaRecursos(models.Model):
    paci = models.ForeignKey(Paci, on_delete=models.CASCADE, verbose_name='PACI', related_name='aula_recursos')
    aula_de_recursos = models.TextField(verbose_name='Aula de Recursos', blank=True, null=True)

    def __str__(self):
        return f'{self.aula_de_recursos}'

class AulaRegular(models.Model):
    paci = models.ForeignKey(Paci, on_delete=models.CASCADE, verbose_name='PACI', related_name='aula_regular')
    aula_regular = models.TextField(verbose_name='Aula Regular', blank=True, null=True)

    def __str__(self):
        return f'{self.aula_regular}'

# 5. ADECUACIÓN DE ACCESO
class PresentacionRepresentacion(models.Model):
    paci = models.ForeignKey(Paci, on_delete=models.CASCADE, verbose_name='PACI', related_name='presentacion_representacion')
    presentacion_representacion = models.TextField(verbose_name='Presentación y Representación de la Información', blank=True, null=True)

    def __str__(self):
        return f'{self.presentacion_representacion}'

class MediosEjecucionExpresion(models.Model):
    paci = models.ForeignKey(Paci, on_delete=models.CASCADE, verbose_name='PACI', related_name='medios_ejecucion_expresion')
    medios_ejecucion_expresion = models.TextField(verbose_name='Medios de Ejecución y Expresión', blank=True, null=True)

    def __str__(self):
        return f'{self.medios_ejecucion_expresion}'

class MultiplesMedios(models.Model):
    paci = models.ForeignKey(Paci, on_delete=models.CASCADE, verbose_name='PACI', related_name='multiples_medios')
    multiples_medios = models.TextField(verbose_name='Proporcionar múltiples medios de participación y compromiso', blank=True, null=True)

    def __str__(self):
        return f'{self.multiples_medios}'

class Entorno(models.Model):
    paci = models.ForeignKey(Paci, on_delete=models.CASCADE, verbose_name='PACI', related_name='entorno')
    entorno = models.TextField(verbose_name='Entorno (Adecuación en los espacios, ubicación y condiciones)', blank=True, null=True)

    def __str__(self):
        return f'{self.entorno}'

class OrganizacionTiempo(models.Model):
    paci = models.ForeignKey(Paci, on_delete=models.CASCADE, verbose_name='PACI', related_name='organizacion_tiempo')
    organizacion_tiempo = models.TextField(verbose_name='Organización del tiempo y el horario', blank=True, null=True)

    def __str__(self):
        return f'{self.organizacion_tiempo}'

# 6. ADECUACIÓN DE OBJETIVOS
class GraduacionComplejidad(models.Model):
    paci = models.ForeignKey(Paci, on_delete=models.CASCADE, verbose_name='PACI', related_name='graduacion_complejidad')
    graduacion_complejidad = models.TextField(verbose_name='Graduación del nivel de complejidad', blank=True, null=True)

    def __str__(self):
        return f'{self.graduacion_complejidad}'

class PriorizacionOA(models.Model):
    paci = models.ForeignKey(Paci, on_delete=models.CASCADE, verbose_name='PACI', related_name='priorizacion_oa')
    priorizacion_oa = models.TextField(verbose_name='Priorización de OA y contenidos', blank=True, null=True)

    def __str__(self):
        return f'{self.priorizacion_oa}'

class Temporalizacion(models.Model):
    paci = models.ForeignKey(Paci, on_delete=models.CASCADE, verbose_name='PACI', related_name='temporalizacion')
    temporalizacion = models.TextField(verbose_name='Temporalización', blank=True, null=True)

    def __str__(self):
        return f'{self.temporalizacion}'

class EnriquecimientoCurriculum(models.Model):
    paci = models.ForeignKey(Paci, on_delete=models.CASCADE, verbose_name='PACI', related_name='enriquecimiento_curriculum')
    enriquecimiento_curriculum = models.TextField(verbose_name='Enriquecimiento del Curriculum', blank=True, null=True)

    def __str__(self):
        return f'{self.enriquecimiento_curriculum}'

# 7. OBJETIVOS DE APRENDIZAJE
class ObjetivosAprendizaje(models.Model):
    paci = models.ForeignKey(Paci, on_delete=models.CASCADE, verbose_name='PACI', related_name='objetivos_aprendizaje')
    nivel_ensenanza = models.CharField(max_length=150, choices=opciones_educacion, verbose_name='Nivel de Enseñanza', blank=True, null=True)
    curso = models.CharField(max_length=350, verbose_name='Curso', blank=True, null=True)
    asignatura_o_nucleo = models.CharField(max_length=350, verbose_name='Asignatura o Núcleo', blank=True, null=True)
    eje_o_ambito = models.CharField(max_length=350, verbose_name='Eje o Ámbito', blank=True, null=True)
    espacio_educativo = models.CharField(max_length=350, verbose_name='Contexto o Espacio Educativo', blank=True, null=True)

    def __str__(self):
        return f'{self.nivel_ensenanza} - {self.curso} - {self.asignatura_o_nucleo} - {self.eje_o_ambito} - {self.espacio_educativo}'   
    

    #ESTO VA EN COLUMNAS
class ColumnasObjetivosAprendizaje(models.Model):
    paci = models.ForeignKey(Paci, on_delete=models.CASCADE, verbose_name='PACI', related_name='columnas_objetivos_aprendizaje')
    codigo = models.CharField(max_length=150, verbose_name='Código', blank=True, null=True)
    objetivos_aprendizaje = models.TextField(verbose_name='Objetivos de Aprendizaje Priorizados', blank=True, null=True)
    adaptacion_de_oa = models.TextField(verbose_name='Adaptación de OA', blank=True, null=True)
    estrategias_metodologicas = models.TextField(verbose_name='Estrategias Metodológicas', blank=True, null=True)
    evaluacion_de_oa = models.TextField(verbose_name='Evaluación de OA', blank=True, null=True)

    def __str__(self):
        return f'{self.codigo} - {self.objetivos_aprendizaje} - {self.adaptacion_de_oa} - {self.estrategias_metodologicas} - {self.evaluacion_de_oa}'

# 8. COLABORACIÓN DE LA FAMILIA
class ColaboracionFamilia(models.Model):
    paci = models.ForeignKey(Paci, on_delete=models.CASCADE, verbose_name='PACI', related_name='colaboracion_familia')
    aspectos_familia = models.TextField(verbose_name='Aspectos a Considerar', blank=True, null=True)

    def __str__(self):
        return f'{self.aspectos_familia}'

# 9. CRITERIOS DE EVALUACIÓN Y PROMOCIÓN
class CritEvaluacionPromocion(models.Model):
    paci = models.ForeignKey(Paci, on_delete=models.CASCADE, verbose_name='PACI', related_name='crit_evaluacion_promocion')
    criterios = models.TextField(verbose_name='Aspectos a Considerar', blank=True, null=True)

    def __str__(self):
        return f'{self.criterios}'

# 10. SEGUIMIENTO DE PACI
class SeguimientoPaci(models.Model):
    paci = models.ForeignKey(Paci, on_delete=models.CASCADE, verbose_name='PACI', related_name='seguimiento_paci')
    seguimiento = models.TextField(verbose_name='Aspectos a Considerar', blank=True, null=True)

    def __str__(self):
        return f'{self.seguimiento}'

# 11. FIRMA EQUIPO RESPONSABLE PACI
class FirmaPaci(models.Model):
    paci = models.ForeignKey(Paci, on_delete=models.CASCADE, verbose_name='PACI', related_name='firma_paci')
    nombre = models.CharField(max_length=150, verbose_name='Nombre', blank=True, null=True)
    cargo = models.CharField(max_length=150, verbose_name='Cargo', blank=True, null=True)

    def __str__(self):
        return f'{self.nombre} - {self.cargo}'