import pytest
"""
Pruebas para la verificación del RUT (Rol Único Tributario).
Estas pruebas verifican la funcionalidad del endpoint de verificación de RUT para asegurar
que los RUT válidos sean identificados correctamente y los RUT inválidos sean rechazados.
Funciones:
    test_verificar_dv_rut_valido(client): Prueba la verificación de un RUT válido.
    test_verificar_dv_rut_invalido(client): Prueba la verificación de un RUT inválido.
"""
from django.urls import reverse
from django.test import Client
from django.contrib.auth import get_user_model
from accounts.models import Profile

@pytest.mark.django_db
def test_verificar_dv_rut_valido(client):
    # Hacer una solicitud GET con un RUT válido
    response = client.get(reverse('verificar_dv_rut'), {'rut': '14.106.615-3'})
    
    # Verificar que la respuesta sea un código 200
    assert response.status_code == 200
    
    # Verificar que el dígito verificador sea válido
    assert response.json() == {'es_valido': True}

@pytest.mark.django_db
def test_verificar_dv_rut_invalido(client):
    # Hacer una solicitud GET con un RUT inválido (cambiando el guion)
    response = client.get(reverse('verificar_dv_rut'), {'rut': '14.106.615-4'})
    
    # Verificar que la respuesta sea un código 200
    assert response.status_code == 200
    
    # Verificar que el dígito verificador sea inválido
    assert response.json() == {'es_valido': False}