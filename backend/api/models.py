# api/models.py
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def _create_user(self, dni, apel_nomb, password=None, **extra_fields):
        if not dni:
            raise ValueError('El campo DNI es obligatorio.')

        user = self.model(
            dni=dni,
            apel_nomb=apel_nomb,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, dni, apel_nomb, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(dni, apel_nomb, password, **extra_fields)

    def create_superuser(self, dni, apel_nomb, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(dni, apel_nomb, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(primary_key=True)
    dni = models.CharField(unique=True, max_length=10)
    apel_nomb = models.CharField(max_length=255)
    tipo_usuarioapp = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'dni'
    REQUIRED_FIELDS = ['apel_nomb', 'tipo_usuarioapp']

    def __str__(self):
        return f'{self.apel_nomb} ({self.dni})'
