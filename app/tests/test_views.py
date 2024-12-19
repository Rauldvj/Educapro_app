import pytest
"""
Este módulo contiene casos de prueba para la vista de inicio de sesión personalizada de la aplicación Django.
Casos de prueba:
- test_custom_login_view_valid: Prueba la funcionalidad de inicio de sesión con credenciales válidas.
- test_custom_login_view_invalid: Prueba la funcionalidad de inicio de sesión con credenciales inválidas.
- test_custom_login_view_redirect_to_password_change: Prueba la funcionalidad de inicio de sesión para usuarios creados por un coordinador, asegurando que sean redirigidos a la página de cambio de contraseña.
Funciones:
- test_custom_login_view_valid(client): 
    - Crea un usuario de prueba.
    - Envía una solicitud POST con credenciales válidas.
    - Verifica que la respuesta sea una redirección (código de estado 302).
    - Verifica que el usuario esté autenticado.
    - Verifica que un mensaje de bienvenida esté presente en los mensajes de la respuesta.
- test_custom_login_view_invalid(client): 
    - Envía una solicitud POST con credenciales inválidas.
    - Verifica que el código de estado de la respuesta sea 200 (formulario inválido).
    - Verifica que el usuario no esté autenticado.
    - Verifica que un mensaje de error sobre nombre de usuario o contraseña incorrectos esté presente en los mensajes de la respuesta.
- test_custom_login_view_redirect_to_password_change(client): 
    - Crea un usuario de prueba con un perfil creado por un coordinador.
    - Envía una solicitud POST con credenciales válidas.
    - Verifica que la respuesta sea una redirección a la página de cambio de contraseña (código de estado 302).
    - Verifica que un mensaje sobre cambiar la contraseña esté presente en los mensajes de la respuesta.
"""
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages

@pytest.mark.django_db
def test_custom_login_view_valid(client):
    # Crear un usuario de prueba
    user = get_user_model().objects.create_user(username='testuser', password='testpassword')
    
    # Hacer una solicitud POST con credenciales válidas
    response = client.post(reverse('custom_login'), {'username': 'testuser', 'password': 'testpassword'})
    
    # Verificar que la respuesta sea una redirección
    assert response.status_code == 302
    
    # Verificar que el usuario esté autenticado
    assert response.wsgi_request.user.is_authenticated
    
    # Verificar los mensajes
    messages = list(get_messages(response.wsgi_request))
    assert any('Bienvenido' in str(message) for message in messages)

@pytest.mark.django_db
def test_custom_login_view_invalid(client):
    # Hacer una solicitud POST con credenciales inválidas
    response = client.post(reverse('custom_login'), {'username': 'wronguser', 'password': 'wrongpassword'})
    
    # Verificar que la respuesta sea un código 200 (formulario inválido)
    assert response.status_code == 200
    
    # Verificar que el usuario no esté autenticado
    assert not response.wsgi_request.user.is_authenticated
    
    # Verificar los mensajes
    messages = list(get_messages(response.wsgi_request))
    assert any('Nombre de usuario o contraseña incorrectos' in str(message) for message in messages)

@pytest.mark.django_db
def test_custom_login_view_redirect_to_password_change(client):
    # Crear un usuario de prueba con el perfil creado por el coordinador
    user = get_user_model().objects.create_user(username='testuser', password='testpassword')
    user.profile.creado_por_coordinador = True
    user.profile.save()
    
    # Hacer una solicitud POST con credenciales válidas
    response = client.post(reverse('custom_login'), {'username': 'testuser', 'password': 'testpassword'})
    
    # Verificar que la respuesta sea una redirección a la página de cambio de contraseña
    assert response.status_code == 302
    assert response.url == reverse('profile_password_change')
    
    # Verificar los mensajes
    messages = list(get_messages(response.wsgi_request))
    assert any('Bienvenido, debe cambiar su contraseña ahora' in str(message) for message in messages)