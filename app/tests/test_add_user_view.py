import pytest
"""
Este módulo contiene pruebas unitarias para la vista de agregar usuario en una aplicación Django.
Autores:
- Raúl Córdova Vicencio
- Francisca Olavarría Pavez
- Carlos Olivero Bruno
Fecha de elaboración: 15 diciembre 2024
Funciones:
- test_add_user_view_permission(client): Verifica que un usuario con permisos de coordinador puede acceder a la vista de agregar usuario.
- test_add_user_view_no_permission(client): Verifica que un usuario sin permisos no puede acceder a la vista de agregar usuario y es redirigido a una página de error.
- test_add_user_view_form_valid(client): Verifica que un usuario con permisos puede enviar un formulario válido para crear un nuevo usuario y es redirigido a la página de perfil.
- test_add_user_view_form_invalid(client): Verifica que un usuario con permisos no puede enviar un formulario inválido (contraseñas que no coinciden) y recibe un código de respuesta 200 indicando que el formulario es inválido.
"""
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.test import Client
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages

@pytest.mark.django_db
def test_add_user_view_permission(client):
    # Crear un usuario coordinador
    coordinador_group = Group.objects.create(name='Coordinadores')
    coordinador = get_user_model().objects.create_user(username='coordinador', password='testpassword')
    coordinador.groups.add(coordinador_group)
    
    # Autenticar al usuario coordinador
    client.login(username='coordinador', password='testpassword')
    
    # Hacer una solicitud GET a la vista de registro de usuario
    response = client.get(reverse('add_user'))
    
    # Verificar que la respuesta sea un código 200 (permiso concedido)
    assert response.status_code == 200

@pytest.mark.django_db
def test_add_user_view_no_permission(client):
    # Crear un usuario sin permisos
    user = get_user_model().objects.create_user(username='user', password='testpassword')
    
    # Autenticar al usuario sin permisos
    client.login(username='user', password='testpassword')
    
    # Hacer una solicitud GET a la vista de registro de usuario
    response = client.get(reverse('add_user'))
    
    # Verificar que la respuesta sea una redirección a la página de error (permiso denegado)
    assert response.status_code == 302
    assert response.url == reverse('error')

@pytest.mark.django_db
def test_add_user_view_form_valid(client):
    # Crear un usuario coordinador
    coordinador_group = Group.objects.create(name='Coordinadores')
    coordinador = get_user_model().objects.create_user(username='coordinador', password='testpassword')
    coordinador.groups.add(coordinador_group)
    
    # Autenticar al usuario coordinador
    client.login(username='coordinador', password='testpassword')
    
    # Datos del nuevo usuario
    new_user_data = {
        'username': 'newuser',
        'password1': 'newpassword123',
        'password2': 'newpassword123',
        'apellido_paterno': 'ApellidoPaterno',
        'apellido_materno': 'ApellidoMaterno',
        'rut': '12345678-9',
        'group': coordinador_group.id
    }
    
    # Hacer una solicitud POST con datos válidos
    response = client.post(reverse('add_user'), new_user_data)
    
    # Verificar que la respuesta sea una redirección a la página de perfil
    assert response.status_code == 302
    assert response.url == reverse('profile')
    
    # Verificar que el nuevo usuario se haya creado
    new_user = get_user_model().objects.get(username='newuser')
    assert new_user is not None
    
    # Verificar los mensajes
    messages = list(get_messages(response.wsgi_request))
    assert any('Usuario creado exitosamente' in str(message) for message in messages)

@pytest.mark.django_db
def test_add_user_view_form_invalid(client):
    # Crear un usuario coordinador
    coordinador_group = Group.objects.create(name='Coordinadores')
    coordinador = get_user_model().objects.create_user(username='coordinador', password='testpassword')
    coordinador.groups.add(coordinador_group)
    
    # Autenticar al usuario coordinador
    client.login(username='coordinador', password='testpassword')
    
    # Datos del nuevo usuario con contraseñas que no coinciden
    new_user_data = {
        'username': 'newuser',
        'password1': 'newpassword123',
        'password2': 'differentpassword',
        'apellido_paterno': 'ApellidoPaterno',
        'apellido_materno': 'ApellidoMaterno',
        'rut': '12345678-9',
        'group': coordinador_group.id
    }
    
    # Hacer una solicitud POST con datos inválidos
    response = client.post(reverse('add_user'), new_user_data)
    
    # Verificar que la respuesta sea un código 200 (formulario inválido)
    assert response.status_code == 200
    
    # Verificar que el nuevo usuario no se haya creado
    with pytest.raises(get_user_model().DoesNotExist):
        get_user_model().objects.get(username='newuser')