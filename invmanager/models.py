from datetime import datetime, time, date, timedelta
import time

from django.db import models
from django.conf import settings
import uuid
from tinymce.models import HTMLField
from graphviz import *
from django.contrib.auth.models import User

APPOINTMENT_CHOICE = (
    ("MAIN", "Maintenance"),
    ("INS", "Inspection"),
    ("REPL", "Replacement")
)


class Location(models.Model):
    create_datetime = models.DateTimeField('Creation date', auto_now_add=True, null=True)
    modified_datetime = models.DateTimeField('Last changes', null=True, blank=True, auto_now=True)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, verbose_name='Public Identifier')

    street = models.CharField('Street', max_length=150, blank=True)
    house_number = models.CharField('House number', max_length=150, blank=True)
    postal_code = models.CharField('Postal code', max_length=150, blank=True)
    city = models.CharField('City', max_length=150, blank=False)
    country = models.CharField('Country', max_length=150, blank=True)

    def __str__(self):
        return self.city + ' ' + self.country


class GadgetType(models.Model):
    create_datetime = models.DateTimeField('Creation date', auto_now_add=True, null=True)
    modified_datetime = models.DateTimeField('Last changes', null=True, blank=True, auto_now=True)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, verbose_name='Public Identifier')

    type = models.CharField('Type', max_length=150)

    def __str__(self):
        return self.type


class Company(models.Model):
    create_datetime = models.DateTimeField('Creation date', auto_now_add=True, null=True)
    modified_datetime = models.DateTimeField('Last changes', null=True, blank=True, auto_now=True)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, verbose_name='Public Identifier')

    name = models.CharField('Company name', max_length=150, blank=False, null=False, unique=True)
    email = models.EmailField('E-Mail', max_length=150, blank=True)
    location = models.ManyToManyField(Location)
    is_craft_enterprise = models.BooleanField(default=False, blank=False, null=False)
    type = models.ManyToManyField(GadgetType, blank=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Appointment(models.Model):
    create_datetime = models.DateTimeField('Creation date', auto_now_add=True, null=True)
    modified_datetime = models.DateTimeField('Last changes', null=True, blank=True, auto_now=True)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, verbose_name='Public Identifier')

    type = models.CharField('Type', choices=APPOINTMENT_CHOICE, max_length=500)

    #replacement/maintenance/inspection
    interval = models.IntegerField('Interval', null=False, blank=True)
    last_appointment = models.DateField('Last appointment', null=False, blank=True)
    next_appointment = models.DateField('Next appointment', null=True, blank=True)

    additional_information = models.TextField('Additional information', blank=True)

    def save(self, *args, **kwargs):
        self.compute_next_appointment()
        super(Appointment, self).save(*args, **kwargs)

    def compute_next_appointment(self, *args, **kwargs):
        self.full_clean()
        self.next_appointment = self.last_appointment + timedelta(weeks=self.interval)

    def __str__(self):
        return self.type + ' ' + str(self.last_appointment) + ' ' + str(self.interval)


class Gadget(models.Model):
    create_datetime = models.DateTimeField('Creation date', auto_now_add=True, null=True)
    modified_datetime = models.DateTimeField('Last changes', null=True, blank=True, auto_now=True)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, verbose_name='Public Identifier')

    name = models.CharField('Name', max_length=150, null=False, blank=True)
    number = models.IntegerField('Machinery number', null=False, blank=False)
    type = models.ForeignKey(GadgetType, null=True, blank=False, on_delete=models.SET_NULL)
    image = models.ImageField('Image', height_field=None, width_field=None, max_length=100, null=True, blank=True)

    date_of_installation = models.DateField('Date of installation', null=False, blank=True)

    appointments = models.ManyToManyField(Appointment, blank=True)

    replacement_interval = models.IntegerField('Replacement time', null=False, blank=True)
    replacement_date = None

    location = models.ForeignKey('Location', Location, blank=False, null=False)
    company = models.ForeignKey('Company', Company, blank=False, null=False)

    def calc_replacement_date(self):
        return self.date_of_installation.day + self.replacement_interval * 7

    def __str__(self):
        return self.name + ' ' + str(self.number) + ' ' + str(self.type)


class Employee(models.Model):
    create_datetime = models.DateTimeField('Creation date', auto_now_add=True, null=True)
    modified_datetime = models.DateTimeField('Last changes', null=True, blank=True, auto_now=True)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, verbose_name='Public Identifier')

    last_name = models.CharField('Last name', max_length=150, blank=False, null=False)
    first_name = models.CharField('First name', max_length=150, blank=False, null=False)
    email = models.EmailField('E-Mail', max_length=150, blank=True)
    is_active = models.BooleanField(default=True)

    company = models.ForeignKey('Company', Company, blank=False, null=False)
    gadget = models.ManyToManyField(Gadget, blank=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    class Meta:
        permissions = (
        )

    def __str__(self):
        return self.last_name + ' ' + self.first_name + ' ' + str(self.company)


