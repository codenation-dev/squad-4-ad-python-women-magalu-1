from django.db import models
from django.db.models import Q, QuerySet
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import MinLengthValidator, EmailValidator, validate_ipv4_address

import datetime

# Create your models here.
LEVEL_CHOICES = [
    ('critical', 'Critical'),
    ('debug', 'Debug'),
    ('error', 'Error'),
    ('warning', 'Warning'),
    ('information', 'Info'),
]

min_validator = MinLengthValidator(8, 'A senha deve conter pelo menos 8 caracteres.')


class EventManager(models.Manager):
    def environment(self, pk: int, order: str) -> QuerySet:
        """
            Realiza a pesquisa nos eventos cujo ambiente seja do id **pk**.

            :param text: Texto que será usado na pesquisa

            :return: QuerySet com o filtro aplicado
        """
        queryset = self.get_queryset().filter(environment=pk).order_by(order)
        return queryset

    def level_with_text(self, text: str) -> QuerySet:
        """
            Realiza a pesquisa nos eventos cujo o nome do tipo de evento contenha **text**.

            :param text: Texto que será usado na pesquisa

            :return: QuerySet com o filtro aplicado
        """
        queryset = self.get_queryset().filter(level__name__contains=text).order_by(order)
        return queryset

    def environment_with_text(self, text: str) -> QuerySet:
        """
            Realiza a pesquisa nos eventos cujo o ambiente do evento contenha **text**.

            :param text: Texto que será usado na pesquisa

            :return: QuerySet com o filtro aplicado
        """
        queryset = self.get_queryset().filter(environment__name__contains=text).order_by(order)
        return queryset

    def data_with_text(self, text: str) -> QuerySet:
        """
            Realiza a pesquisa nos eventos cuja descrição contenha **text**.

            :param text: Texto que será usado na pesquisa

            :return: QuerySet com o filtro aplicado
        """
        queryset = self.get_queryset().filter(data__contains=text).order_by(order)
        return queryset


class UserManager(BaseUserManager):
    def create_user(self, email, name, password, is_staff=False, is_superuser=False, is_active=True):
        user = self.model(email=email, name=name, password=password, is_staff=is_staff, is_superuser=is_superuser, is_active=is_active)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, name, password):
        self.create_user(email, name, password, True, True)
        
        
class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=50)
    email = models.EmailField(validators=[EmailValidator], unique=True)
    password = models.CharField(max_length=50, validators=[min_validator])
    last_login = models.DateField(default=datetime.date.today)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'password']

    objects = UserManager()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Environment(models.Model):
    name = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Agent(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    address = models.GenericIPAddressField(validators=[validate_ipv4_address], null=True)
    status = models.BooleanField(default=False)
    environment = models.ForeignKey(Environment, on_delete=models.PROTECT)
    version = models.CharField(max_length=5)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Level(models.Model):
    name = models.CharField(max_length=20, choices=LEVEL_CHOICES)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Event(models.Model):
    level = models.ForeignKey(Level, on_delete=models.PROTECT)
    data = models.TextField(max_length=500)
    agent = models.OneToOneField(Agent, on_delete=models.PROTECT)
    shelved = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.level +' in ' + self.agent.name

    class Meta:
        ordering = ['date']
