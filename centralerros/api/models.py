from django.core.validators import MinLengthValidator, EmailValidator, validate_ipv4_address
from django.db import models
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


class Group(models.Model):
    name = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class User(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(validators=[EmailValidator])
    password = models.CharField(max_length=50, validators=[min_validator])
    last_login = models.DateField(default=datetime.date.today)
    group = models.ManyToManyField(Group)

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
