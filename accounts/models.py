"""
Autores:
- Raúl Córdova Vicencio
- Francisca Olavarría Pavez
- Carlos Olivero Bruno
Fecha: 01 diciembre 2024
"""

from django.db import models
from django.core.exceptions import ValidationError
from localidad.models import Region, Comuna
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Profile(models.Model):
    """
    Modelo para almacenar la información del perfil del usuario.
    
    Atributos:
        user (ForeignKey): Relación uno a uno con el modelo User.
        image (ImageField): Imagen de perfil del usuario.
        rut (CharField): RUT del usuario.
        direccion (CharField): Dirección del usuario.
        region (ForeignKey): Región del usuario.
        comuna (ForeignKey): Comuna del usuario.
        telefono (CharField): Teléfono del usuario.
        creado_por_coordinador (BooleanField): Indica si el perfil fue creado por un coordinador.
        apellido_paterno (CharField): Apellido paterno del usuario.
        apellido_materno (CharField): Apellido materno del usuario.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='Usuario')
    image = models.ImageField(default='default.png', upload_to='users/', verbose_name='Imagen de perfil')
    rut = models.CharField(max_length=12, unique=True, verbose_name='Rut')
    direccion = models.CharField(max_length=150, null=True, blank=True, verbose_name='Dirección')
    region = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name='Región', blank=True, null=True)
    comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE, verbose_name='Comuna', blank=True, null=True)
    telefono = models.CharField(max_length=9, null=True, blank=True, verbose_name='Teléfono')
    creado_por_coordinador = models.BooleanField(default=True, blank=True, null=True, verbose_name='Creado por el Coordinador')
    apellido_paterno = models.CharField(max_length=50, null=True, blank=True, verbose_name='Apellido Paterno')
    apellido_materno = models.CharField(max_length=50, null=True, blank=True, verbose_name='Apellido Materno')

    class Meta:
        verbose_name = 'perfil'
        verbose_name_plural = 'perfiles'
        ordering = ['-id']

    def __str__(self):
        """
        Retorna una representación en cadena del perfil del usuario.
        
        Returns:
            str: Nombre completo del usuario.
        """
        return f'{self.user.first_name} {self.apellido_paterno} {self.apellido_materno}'

    def clean(self):
        """
        Valida que el RUT sea único.
        
        Raises:
            ValidationError: Si el RUT ya existe.
        """
        super().clean()
        if Profile.objects.filter(rut=self.rut).exclude(pk=self.pk).exists():
            raise ValidationError({'rut': 'Este RUT ya existe!'})

def create_user_profile(sender, instance, created, **kwargs):
    """
    Crea un perfil de usuario cuando se crea un nuevo usuario.
    
    Args:
        sender (Model): El modelo que envía la señal.
        instance (User): La instancia del usuario.
        created (bool): Indica si el usuario fue creado.
        **kwargs: Argumentos adicionales.
    """
    if created:
        default_region = Region.objects.first()
        default_comuna = Comuna.objects.first()
        Profile.objects.create(user=instance, region=default_region, comuna=default_comuna)

def save_user_profile(sender, instance, **kwargs):
    """
    Guarda el perfil del usuario cuando se guarda el usuario.
    
    Args:
        sender (Model): El modelo que envía la señal.
        instance (User): La instancia del usuario.
        **kwargs: Argumentos adicionales.
    """
    instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)