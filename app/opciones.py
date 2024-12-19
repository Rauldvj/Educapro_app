#Este archivo opciones.py, se crea con la finalidad de escribir ciertas funciones que
#no necesitan ser heredadas por los modelos, pero si para ser utilizadas como opciones en el
#Estos módulos de opciones serán llamados en el archivo modelos.py

opciones_aprendizaje = (
    ('No logrado', 'No logrado'),
    ('Via de logro', 'Via de logro'),
    ('Logrado', 'Logrado')
)

opciones_si_no = (
    ('Si','Si'),
    ('No','No')
)

opcionesBloque = (
    ('Primer bloque', 'Primer bloque'),
    ('Segundo bloque', 'Segundo bloque'),
    ('Tercer bloque', 'Tercer bloque'),
    ('Cuarto bloque', 'Cuarto bloque'),
)

opcionesSexo = (
    ('0', 'Femenino'),
    ('1', 'Masculino')
)

opciones_lengua = (
    ('Seleccione', 'Seleccione'),
    ('Español', 'Español'),
    ('Ingles', 'Ingles'),
    ('Chino', 'Chino'),
    ('Aymara', 'Aymara'),
    ('Quechua', 'Quechua'),
    ('Mapudungu', 'Mapudungu'),
)

opcion_relacion = (
    ('Seleccione', 'Seleccione'),
    ('Padre', 'Padre'),
    ('Madre', 'Madre'),
    ('Abuelo', 'Abuelo'),
    ('Abuela', 'Abuela'),
    ('Hermano', 'Hermano'),
    ('Hermana', 'Hermana'),
    ('Tio', 'Tio'),
    ('Tia', 'Tia'),
    ('Otro', 'Otro'),
)

opcion_presencia = (
    ('Seleccione', 'Seleccione'),
    ('Miembro de la familia', 'Miembros de la familia'),
    ('intérpretes', 'intérprete'),
    ('Otro/a', 'Otro/a'),
)

opcion_parto = (
    ('Normal', 'Normal'),
    ('Inducido', 'Inducido'),
    ('Fórceps', 'Fórceps'),
    ('Cesárea', 'Cesárea'),
)

opcion_d_n = (
    ('Diurno', 'Diurno'),
    ('Nocturno', 'Nocturno'),
)

opcion_actividad_motora = (
    ('Normal', 'Normal'),
    ('Activo', 'Activo'),
    ('Hiperactivo', 'Hiperactivo'),
    ('Hipoactivo', 'Hipoactivo'),
)

#________________________________________#

opcion_tono_muscular = (
    ('Normal', 'Normal'),
    ('Hipertónico', 'Hipertónico'),
    ('Hipotónico', 'Hipotónico'),
)

#______________________________________#

opcion_comunica = (
    ('Oral ', 'Oral'),
    ('Gestual', 'Gestual'),
    ('Mixto', 'Mixto'),
    ('Otro', 'Otro'),
)

#______________________________________#

opcion_estimulos = (
    ('Natural', 'Natural'),
    ('Desmesurada', 'Desmesurada'),
)

opcion_alimentacion = (
    ('Normal', 'Normal'),
    ('“Malo/a” para comer', '“Malo/a” para comer'),
    ('“Bueno/a” para comer', '“Bueno/a” para comer'),
    ('Otro (especifique):', 'Otro (especifique):'),
)

#______________________________________#

opcion_peso = (
    ('Normal', 'Normal'),
    ('Bajo peso', 'Bajo peso'),
    ('Obesidad', 'Obesidad'),
)

#______________________________________#

opcion_sueno = (
    ('Normal', 'Normal'),
    ('Tranquilo', 'Tranquilo'),
    ('Inquieto', 'Inquieto'),
)

#______________________________________#

opcion_como_duerme = (
    ('Solo', 'Solo'),
    ('Acompañado', 'Acompañado'),
)