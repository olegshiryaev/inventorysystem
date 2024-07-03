from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    last_name = models.CharField(max_length=30, blank=True, verbose_name="Фамилия")
    first_name = models.CharField(max_length=30, blank=True, verbose_name="Имя")
    middle_name = models.CharField(max_length=30, blank=True, null=True, verbose_name="Отчество")
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name="Адрес")
    position = models.CharField(max_length=100, blank=True, null=True, verbose_name="Должность")
    department = models.CharField(max_length=100, blank=True, null=True, verbose_name="Отдел")
    employee_number = models.CharField(max_length=100, blank=True, null=True, unique=True, verbose_name="Табельный номер")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Телефон")
    supervisor = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subordinates', verbose_name="Руководитель"
    )
    is_mol = models.BooleanField(default=False, verbose_name="Является МОЛом")
    is_active = models.BooleanField(default=True, verbose_name="Аккаунт активен")
    is_staff = models.BooleanField(default=False, verbose_name="Администратор")
    date_joined = models.DateTimeField(default=timezone.now, verbose_name="Дата регистрации")

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}".strip()
    
    def __str__(self):
        return f"{self.email}"
    
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"