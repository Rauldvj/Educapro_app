"""
Autores:
- Raúl Córdova Vicencio
- Francisca Olavarría Pavez
- Carlos Olivero Bruno
Fecha: 01 diciembre 2024
"""

from django import forms #IMPORTAMOS LOS FORMULARIOS
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm #IMPORTAMOS EL FORMULARIO DE AUTENTICACIÓN
from django.contrib.auth.models import User #IMPORTAMOS EL MODELO DE USUARIOS
from .models import * #IMPORTAMOS LOS MODELOS
from accounts.models import Profile, Region, Comuna


# FORMULARIO LOGIN
class LoginForm(AuthenticationForm):
    """
    Formulario de autenticación para el login de usuarios.
    """
    pass



#____________________________________________________________________________________________________________________________    
# CREAR EL FORMULARIO QUE HEREDA LOS DATOS DEL USER
class UserForm(forms.ModelForm):
    """
    Formulario para actualizar la información del usuario.
    
    Atributos:
        model (User): El modelo relacionado.
        fields (list): Campos a mostrar en el formulario.
    """
    class Meta:
        model = User #IMPORTAMOS EL MODELO DE USUARIOS
        fields = ['first_name', 'email']



#____________________________________________________________________________________________________________________________
# FORMULARIO DE PERFIL

class ProfileForm(forms.ModelForm):
    """
    Formulario para actualizar la información del perfil del usuario.
    
    Atributos:
        region (ModelChoiceField): Campo para seleccionar la región.
        comuna (ModelChoiceField): Campo para seleccionar la comuna.
        model (Profile): El modelo relacionado.
        fields (list): Campos a mostrar en el formulario.
        widgets (dict): Widgets personalizados para los campos.
    """
    region = forms.ModelChoiceField(queryset=Region.objects.all(), widget=forms.Select(attrs={'class': 'bg-white text-gray-900 rounded-xl pl-2 py-1 md:py-2 text-sm focus:outline-none w-full'}))
    comuna = forms.ModelChoiceField(queryset=Comuna.objects.all(), widget=forms.Select(attrs={'class': 'bg-white text-gray-900 rounded-xl pl-2 py-1 md:py-2 text-sm focus:outline-none w-full'}))

    class Meta:
        model = Profile
        fields = ['image', 'apellido_paterno', 'apellido_materno', 'direccion', 'region', 'comuna', 'telefono']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'bg-white text-gray-900 rounded-xl pl-2 py-1 md:py-2 text-sm focus:outline-none w-full'
            }),

            'apellido_paterno': forms.TextInput(attrs={
                'class': 'bg-white text-gray-900 rounded-xl pl-2 py-1 md:py-2 text-sm focus:outline-none w-full',
                'placeholder': 'Apellido Paterno'
            }),
            'apellido_materno': forms.TextInput(attrs={
                'class': 'bg-white text-gray-900 rounded-xl pl-2 py-1 md:py-2 text-sm focus:outline-none w-full',
                'placeholder': 'Apellido Materno'
            }),
            'direccion': forms.TextInput(attrs={
                'class': 'bg-white text-gray-900 rounded-xl pl-2 py-1 md:py-2 text-sm focus:outline-none w-full',
                'placeholder': 'Ejemplo: Calle 123'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'bg-white text-gray-900 rounded-xl pl-2 py-1 md:py-2 text-sm focus:outline-none w-full',
                'placeholder': 'Ejemplo: 987654321'
            })
        }


#____________________________________________________________________________________________________________________________

# FORMULARIO PARA REGISTRO DE NUEVO USUARIO CREADO POR EL COORDINADOR
class UserCreationForm(forms.ModelForm):
    """
    Formulario para la creación de un nuevo usuario por el coordinador.
    
    Atributos:
        apellido_paterno (CharField): Campo para el apellido paterno.
        apellido_materno (CharField): Campo para el apellido materno.
        rut (CharField): Campo para el RUT.
        model (User): El modelo relacionado.
        fields (list): Campos a mostrar en el formulario.
        widgets (dict): Widgets personalizados para los campos.
    """
    apellido_paterno = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'bg-white text-gray-900 rounded-xl pl-2 py-1 md:py-2 text-sm focus:outline-none w-full',
            'placeholder': 'Apellido Paterno',
        })
    )
    apellido_materno = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'bg-white text-gray-900 rounded-xl pl-2 py-1 md:py-2 text-sm focus:outline-none w-full',
            'placeholder': 'Apellido Materno',
        })
    )
    rut = forms.CharField(
        max_length=12,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'rut-input bg-white text-gray-900 rounded-xl pl-2 py-1 md:py-2 text-sm focus:outline-none w-full',
            'placeholder': 'Ejemplo: 11111111-1',
            'maxlength': '12',
        })
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'bg-white text-gray-900 rounded-xl pl-2 py-1 md:py-2 text-sm focus:outline-none w-full',
                'placeholder': 'Nombre de Usuario',
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'bg-white text-gray-900 rounded-xl pl-2 py-1 md:py-2 text-sm focus:outline-none w-full',
                'placeholder': 'Nombres',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'bg-white text-gray-900 rounded-xl pl-2 py-1 md:py-2 text-sm focus:outline-none w-full',
                'placeholder': 'Ejemplo: 7Kqeh@example.com',
            }),
        }

    def clean_rut(self):
        """
        Valida que el RUT no exista en el sistema.
        """
        rut = self.cleaned_data.get('rut')
        if Profile.objects.filter(rut=rut).exists():
            raise forms.ValidationError('Este RUT ya existe en el sistema.')
        return rut

    def save(self, commit=True):
        """
        Guarda el usuario y crea o actualiza el perfil asociado.
        """
        user = super().save(commit=False)
        if commit:
            user.save()
            # Crear o actualizar el perfil asociado
            profile, created = Profile.objects.get_or_create(user=user)
            profile.apellido_paterno = self.cleaned_data['apellido_paterno'].capitalize()
            profile.apellido_materno = self.cleaned_data['apellido_materno'].capitalize()
            profile.rut = self.cleaned_data['rut']
            profile.save()
        return user