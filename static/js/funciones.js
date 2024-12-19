// Este script se encarga de manejar validaciones, formateos y restricciones en los formularios.

// -------------------------------------------------------------------------------------------
// Evento principal: se ejecuta cuando el DOM ha sido cargado por completo.
document.addEventListener('DOMContentLoaded', function () {
    // Solo inicializar las validaciones si existen los elementos correspondientes
    if (document.querySelector('.rut-input')) {
        initRutValidation();
    }
    if (document.querySelector('.fecha-nacimiento-input')) {
        initFechaNacimientoValidation();
    }
    if (document.querySelector('.edad-input')) {
        initEdadValidation();
    }
    if (document.querySelector('.area-select')) {
        initFilterCursos();
    }
    if (document.querySelector('.region-select')) {
        initFilterComunas();
    }
    if (document.querySelector('.cerrar-modal')) {
        initModalClose();
    }
    if (document.querySelector('.renta-input')) {
        initRentaFormatting();
    }
    if (document.querySelector('.fecha-calendario')) {
        initFechaPicker();
        setMaxFechaCalendario();
    }
});

// -------------------------------------------------------------------------------------------
// Función: Validar y formatear el RUT chileno
// -------------------------------------------------------------------------------------------

function initRutValidation() {
    document.querySelectorAll('.rut-input').forEach(rutInput => {
        rutInput.addEventListener('input', formatRutInput);
        rutInput.addEventListener('input', function () {
            const rut = this.value;
            if (rut.length >= 8) {
                // Verificar si el RUT ya existe en la base de datos
                fetch(`/verificar-rut/?rut=${rut}`)
                    .then(response => response.json())
                    .then(data => {
                        const errorMessage = document.getElementById('rut-error');
                        if (data.existe) {
                            if (!errorMessage) {
                                const error = document.createElement('div');
                                error.id = 'rut-error';
                                error.style.color = 'yellow';
                                error.style.fontSize = '0.8rem';
                                error.innerText = '¡Este RUT ya existe!';
                                this.parentNode.appendChild(error);
                            }
                        } else {
                            if (errorMessage) {
                                errorMessage.remove();
                            }
                        }
                    });

                // Verificar el dígito verificador del RUT
                if (rut.includes('-') && rut.split('-')[1].length === 1) {
                    fetch(`/verificar-dv-rut/?rut=${rut}`)
                        .then(response => response.json())
                        .then(data => {
                            const dvErrorMessage = document.getElementById('dv-error');
                            if (!data.es_valido) {
                                if (!dvErrorMessage) {
                                    const error = document.createElement('div');
                                    error.id = 'dv-error';
                                    error.style.color = 'yellow';
                                    error.style.fontSize = '0.8rem';
                                    error.innerText = 'El dígito verificador incorrecto.';
                                    this.parentNode.appendChild(error);
                                }
                            } else {
                                if (dvErrorMessage) {
                                    dvErrorMessage.remove();
                                }
                            }
                        });
                } else {
                    const dvErrorMessage = document.getElementById('dv-error');
                    if (dvErrorMessage) {
                        dvErrorMessage.remove();
                    }
                }
            } else {
                const dvErrorMessage = document.getElementById('dv-error');
                if (dvErrorMessage) {
                    dvErrorMessage.remove();
                }
            }
        });

        // Validar el RUT solo si existe en el formulario
        document.querySelectorAll('form').forEach(form => {
            const rutInputs = form.querySelectorAll('.rut-input');
            if (rutInputs.length > 0) {
                form.addEventListener('submit', function (event) {
                    let rutValid = true;
                    rutInputs.forEach(rutInput => {
                        if (!validarRut(rutInput.value)) {
                            rutInput.classList.add('is-invalid');
                            rutValid = false;
                        }
                    });
                    if (!rutValid) {
                        event.preventDefault();
                        const errorMessage = document.getElementById('rut-error');
                        if (!errorMessage) {
                            const error = document.createElement('div');
                            error.id = 'rut-error';
                            error.style.color = 'red';
                            error.style.fontSize = '0.8rem';
                            error.innerText = 'Debe ingresar un RUT válido.';
                            form.querySelector('.rut-input').parentNode.appendChild(error);
                        }
                    }
                });
            }
        });
    });
}

function formatRutInput(event) {
    let input = event.target;
    input.value = formatRut(input.value);
}

function formatRut(rut) {
    rut = rut.replace(/^0+/, '').replace(/\./g, '').replace(/-/g, '');
    if (rut.length <= 1) return rut;

    let rutNumeros = rut.slice(0, -1);
    let dv = rut.slice(-1);

    let rutFormateado = '';
    while (rutNumeros.length > 3) {
        rutFormateado = '.' + rutNumeros.slice(-3) + rutFormateado;
        rutNumeros = rutNumeros.slice(0, -3);
    }
    rutFormateado = rutNumeros + rutFormateado;

    return rutFormateado + '-' + dv;
}
 
function calcularDV(rutNumeros) {
    let suma = 0;
    let multiplicador = 2;
    for (let i = rutNumeros.length - 1; i >= 0; i--) {
        suma += rutNumeros[i] * multiplicador;
        multiplicador = multiplicador === 7 ? 2 : multiplicador + 1;
    }
    const resto = 11 - (suma % 11);
    if (resto === 11) return '0';
    if (resto === 10) return 'K';
    return String(resto);
}

function validarRut(rut) {
    const rutLimpio = rut.replace(/\./g, '').replace('-', '');
    const rutNumeros = rutLimpio.slice(0, -1);
    const dv = rutLimpio.slice(-1).toUpperCase();
    return calcularDV(rutNumeros) === dv;
}

// -------------------------------------------------------------------------------------------
// Función: Validar y Convertir Fecha de Nacimiento
// -------------------------------------------------------------------------------------------

function initFechaNacimientoValidation() {
    document.querySelectorAll('.fecha-nacimiento-input').forEach(fechaInput => {
        fechaInput.addEventListener('input', function() {
            let value = this.value.replace(/\D/g, ''); // Remover caracteres no numéricos
            if (value.length > 2) {
                value = value.slice(0, 2) + '-' + value.slice(2);
            }
            if (value.length > 5) {
                value = value.slice(0, 5) + '-' + value.slice(5);
            }
            if (value.length > 10) {
                value = value.slice(0, 10); // Limitar a 10 caracteres
            }
            this.value = value;

            // Validación en tiempo real
            const fechaValue = this.value.trim();
            if (fechaValue.length === 10) {
                fetch(`/validar-fecha-nacimiento/?fecha=${fechaValue}`)
                    .then(response => response.json())
                    .then(data => {
                        const errorMessage = document.getElementById('fecha-error');
                        const ageErrorMessage = document.getElementById('age-error');
                        if (!data.es_valida) {
                            if (!errorMessage) {
                                const error = document.createElement('div');
                                error.id = 'fecha-error';
                                error.style.color = 'yellow';
                                error.style.fontSize = '0.8rem';
                                error.innerText = 'Formato de fecha incorrecto.';
                                this.parentNode.appendChild(error);
                            }
                        } else {
                            if (errorMessage) {
                                errorMessage.remove();
                            }
                        }
                        if (data.es_valida && !data.edad_valida) {
                            if (!ageErrorMessage) {
                                const error = document.createElement('div');
                                error.id = 'age-error';
                                error.style.color = 'yellow';
                                error.style.fontSize = '0.8rem';
                                error.innerText = 'La edad debe estar entre 15 y 99 años.';
                                this.parentNode.appendChild(error);
                            }
                        } else {
                            if (ageErrorMessage) {
                                ageErrorMessage.remove();
                            }
                        }

                        // Desactivar el botón de submit si hay errores
                        const submitButton = this.closest('form').querySelector('button[type="submit"]');
                        if (errorMessage || ageErrorMessage) {
                            submitButton.disabled = true;
                        } else {
                            submitButton.disabled = false;
                        }
                    });
            } else {
                const errorMessage = document.getElementById('fecha-error');
                const ageErrorMessage = document.getElementById('age-error');
                if (errorMessage) {
                    errorMessage.remove();
                }
                if (ageErrorMessage) {
                    ageErrorMessage.remove();
                }

                // Desactivar el botón de submit si hay errores
                const submitButton = this.closest('form').querySelector('button[type="submit"]');
                submitButton.disabled = true;
            }
        });
    });
}

// Nueva función para convertir fecha para formulario
function convertirFechaParaFormulario(fechaTexto) {
    const [dia, mes, anio] = fechaTexto.split('-').map(Number);
    return new Date(anio, mes - 1, dia);
}

// -------------------------------------------------------------------------------------------
// Función: Validar edad
// -------------------------------------------------------------------------------------------

function initEdadValidation() {
    const edadInputs = document.querySelectorAll('.edad-input');
    if (edadInputs.length === 0) return; // No continuar si no hay campos de edad

    // Implementar la validación de edad aquí si es necesario
}

// -------------------------------------------------------------------------------------------
// Función: Filtrar cursos según el área académica
// -------------------------------------------------------------------------------------------

function initFilterCursos() {
    document.querySelectorAll('.area-select').forEach(areaSelect => {
        areaSelect.addEventListener('change', function () {
            const cursoSelect = this.closest('div').parentElement.querySelector('.curso-select');
            const areaId = this.value;

            Array.from(cursoSelect.options).forEach(option => {
                const area = option.getAttribute('data-area');
                option.style.display = (area === areaId || areaId === "") ? 'block' : 'none';
            });

            cursoSelect.value = "";
        });
    });
}

// -------------------------------------------------------------------------------------------
// Función: Filtrar comunas según la región
// -------------------------------------------------------------------------------------------

function initFilterComunas() {
    document.querySelectorAll('.region-select').forEach(regionSelect => {
        regionSelect.addEventListener('change', function () {
            const comunaSelect = this.closest('div').parentElement.querySelector('.comuna-select');
            const regionId = this.value;

            Array.from(comunaSelect.options).forEach(option => {
                const region = option.getAttribute('data-region');
                option.style.display = (region === regionId || regionId === "") ? 'block' : 'none';
            });

            comunaSelect.value = "";
        });
    });
}

// -------------------------------------------------------------------------------------------
// Función: Cerrar modales
// -------------------------------------------------------------------------------------------

function initModalClose() {
    document.querySelectorAll('.cerrar-modal').forEach(button => {
        button.addEventListener('click', function () {
            this.closest('dialog').close();
        });
    });
}

// -------------------------------------------------------------------------------------------
// Función: Formateo de renta
// -------------------------------------------------------------------------------------------

function initRentaFormatting() {
    document.querySelectorAll('.renta-input').forEach(rentaInput => {
        rentaInput.value = formatNumber(rentaInput.value.replace(/\./g, ''));
        rentaInput.addEventListener('input', formatRentaInput);
    });
}

function formatRentaInput(event) {
    let input = event.target;
    input.value = formatNumber(input.value.replace(/\D/g, ''));
}

function formatNumber(number) {
    return number.replace(/\B(?=(\d{3})+(?!\d))/g, ".");
}

// -------------------------------------------------------------------------------------------
// Función: Mostrar el selector de fecha al hacer clic en cualquier parte del campo de fecha
// -------------------------------------------------------------------------------------------

function initFechaPicker() {
    document.querySelectorAll('.fecha-calendario').forEach(fechaInput => {
        fechaInput.addEventListener('click', function() {
            this.showPicker();
        });
    });
}

// -------------------------------------------------------------------------------------------
// Función: Establecer la fecha máxima para los campos de fecha
// -------------------------------------------------------------------------------------------

function setMaxFechaCalendario() {
    const today = new Date().toISOString().split('T')[0];
    document.querySelectorAll('.fecha-calendario').forEach(fechaInput => {
        fechaInput.setAttribute('max', today);
    });
}