"""
Autores:
- Raúl Córdova Vicencio
- Francisca Olavarría Pavez
- Carlos Olivero Bruno
Fecha: 01 diciembre 2024
"""

from django import views
from django.urls import path
from django.contrib.auth.decorators import login_required

# IMPORTAMOS LAS CLASES DE VISTAS (VIEWS)
from .views import IndexView, HomeView, ProfileView, superuser_edit, ErrorView, CustomLoginView, ProfilePasswordChangeView\
    , AddUserView, UserDetailView, ResetPasswordView, DesactivarUserView, ActivarUserView\
    , verificar_rut, verificar_dv_rut, validar_fecha_nacimiento
from estudiantes.views import AddEstudianteView, EstudianteDetailView, ApoderadoTitularDetailView \
    , EstudianteUpdateView, ApoderadoTitularUpdateView\
    , AddBitacoraEstudianteView, BitacoraEstudianteListView, BitacoraEstudianteDetailView\
    , BitacoraRedirectView, BitacoraEstudianteUpdateView\
    , PromediosEstudianteView\
    , AnamnesisEstudianteUpdateView, PaiEstudianteUpdateView, PaciEstudianteUpdateView
from pie.views import ListPieView, AddRegistroPieView

# --------------------------------------------------------------------------------------
urlpatterns = [
    # LOGIN PERSONALIZADO

    # URL INDEX (PAGINA PRINCIPAL)
    path('', IndexView.as_view(), name="index"),

    # --------------------------------------------------------------------------------------
    path('verificar-rut/', verificar_rut, name='verificar_rut'),  # Usa la vista importada directamente 
    # --------------------------------------------------------------------------------------
    path('verificar-dv-rut/', verificar_dv_rut, name='verificar_dv_rut'),  # Usa la vista importada directamente
    # --------------------------------------------------------------------------------------
    path('validar-fecha-nacimiento/', validar_fecha_nacimiento, name='validar_fecha_nacimiento'),  # Usa la vista importada directamente
    # --------------------------------------------------------------------------------------
    # URL LOGIN PERSONALIZADO
    path('custom_login/', CustomLoginView.as_view(), name="custom_login"),

    # --------------------------------------------------------------------------------------

    # URL DE PAGINA DE ERROR
    path('error/', login_required(ErrorView.as_view()), name="error"),

    # --------------------------------------------------------------------------------------

    # URL HOME (PAGINA PRINCIPAL)
    path('home/', login_required(HomeView.as_view()), name="home"),

    # --------------------------------------------------------------------------------------

    # URL DEL PERFIL
    path('profile/', login_required(ProfileView.as_view()), name="profile"),

    # --------------------------------------------------------------------------------------

   # URL DE DETALLE DEL USUARIO
    path('profile_detail/<int:pk>/', login_required(UserDetailView.as_view()), name="profile_detail"),

    # EDITAR DATOS DE UN USUARIO
    path('superuser_edit/<int:user_id>', login_required(superuser_edit), name='superuser_edit'),

    # URL DE CAMBIO DE CONTRASEÑA
    path('password_change/', login_required(ProfilePasswordChangeView.as_view()), name="profile_password_change"),

    # URL DE RESET DE CONTRASEÑA
    path('reset_password/<int:user_id>/', login_required(ResetPasswordView.as_view()), name="reset_password"),

    # URL DE ACTIVAR USUARIO
    path('activar_user/<int:user_id>/', login_required(ActivarUserView.as_view()), name="activar_user"),

    # URL DE DESACTIVAR USUARIO
    path('desactivar_user/<int:user_id>/', login_required(DesactivarUserView.as_view()), name="desactivar_user"),

    # AGREGAR NUEVO USUARIO POR EL COORDINADOR O ADMINISTRADOR
    path('add_user/', login_required(AddUserView.as_view()), name="add_user"),

    # URL DE ESTUDIANTES
    path('add_estudiante/', login_required(AddEstudianteView.as_view()), name="add_estudiante"),

    # URL DE EDICIÓN DE ESTUDIANTES
    path('estudiante_edit/<int:pk>/', login_required(EstudianteUpdateView.as_view()), name="estudiante_edit"),

    # URL DE DETALLE DEL ESTUDIANTE
    path('estudiante/<int:pk>/', login_required(EstudianteDetailView.as_view()), name="estudiante"),

    # URL DE DETALLE DEL APODERADOS TITULAR
    path('apoderado_titular/<int:pk>/', login_required(ApoderadoTitularDetailView.as_view()), name="apoderado_titular"),

    # URL PARA EDITAR DATOS DEL APODERADO TITULAR
    path('apoderado_titular_edit/<int:pk>/', login_required(ApoderadoTitularUpdateView.as_view()), name="apoderado_titular_edit"),


    # URL DE LISTADO DE PIE
    path('pie/', login_required(ListPieView.as_view()), name="pie"),

    # URL DE REGISTRO DE PIE
    path('pie_detail/', login_required(AddRegistroPieView.as_view()), name="pie_detail"),

    # URL PARA REGISTRO DE BITACORA DE ESTUDIANTE
    path('bitacora/add/<int:estudiante_id>/', login_required(AddBitacoraEstudianteView.as_view()), name='add_bitacora_estudiante'),

    # URL PARA VISUALIZAR LAS BITACORAS DE UN ESTUDIANTE
    path('bitacora/list/<int:estudiante_id>/', login_required(BitacoraEstudianteListView.as_view()), name='bitacora_estudiante_list'),
    
    # URL PARA REDIRECCIONAR A LA BITACORA DEL DÍA SELECCIONADO
    path('bitacora/redirect/<int:estudiante_id>/', login_required(BitacoraRedirectView.as_view()), name='bitacora_redirect'),
    
    # URL PARA DETALLE DE UNA BITACORA DE UN ESTUDIANTE
    path('bitacora/detail/<int:pk>/', login_required(BitacoraEstudianteDetailView.as_view()), name='bitacora_estudiante'),
    
    # URL PARA EDITAR UNA BITACORA DE UN ESTUDIANTE
    path('bitacora/edit/<int:pk>/', login_required(BitacoraEstudianteUpdateView.as_view()), name='bitacora_estudiante_edit'),
  
    # URL PARA VISUALIZAR LOS PROMEDIOS DE ESTUDIANTE
    path('promedios_estudiante/<int:pk>/', login_required(PromediosEstudianteView.as_view()), name='promedios_estudiante'),

    #INFORMES
    #_____________________________________________________________________________________________________________
    #INFORME DE ANAMNESIS DE UN ESTUDIANTE
    path('anamnesis_estudiante/<int:pk>/', login_required(AnamnesisEstudianteUpdateView.as_view()), name='anamnesis_estudiante'),

    #INFORME DE PAI DE UN ESTUDIANTE
    path('pai_estudiante/<int:pk>/', login_required(PaiEstudianteUpdateView.as_view()), name='pai_estudiante'),

    #INFORME DE PACI DE UN ESTUDIANTE
    path('paci_estudiante/<int:pk>/', login_required(PaciEstudianteUpdateView.as_view()), name='paci_estudiante'),



]