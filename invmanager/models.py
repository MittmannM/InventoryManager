from django.db import models
from django.conf import settings
import uuid
from tinymce.models import HTMLField
from graphviz import *
from django.contrib.auth.models import User

APPOINTMENT_CHOICE = (
    ("Maintenance"),
    ("Inspection"),
    ("Replacement")
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
        return self.city + '/' + self.country + ' [' + str(self.id) + ']'


class MachineryType(models.Model):
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
    type = models.ManyToManyField(MachineryType, blank=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    def __str__(self):
        return self.name + ' [' + str(self.id) + ']'


class Inventory(models.Model):
    create_datetime = models.DateTimeField('Creation date', auto_now_add=True, null=True)
    modified_datetime = models.DateTimeField('Last changes', null=True, blank=True, auto_now=True)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, verbose_name='Public Identifier')

    name = models.CharField('Name', max_length=150, blank=False, null=False)
    product_number = models.CharField('Product number', max_length=100, blank=False, null=False, unique=False)
    quantity = models.IntegerField('Quantity', blank=False, null=False, default=1)
    description = HTMLField('Description', max_length=500, blank=True)
    company = models.ForeignKey('Company', Company, blank=False, null=False)


class Inspection(models.Model):
    create_datetime = models.DateTimeField('Creation date', auto_now_add=True, null=True)
    modified_datetime = models.DateTimeField('Last changes', null=True, blank=True, auto_now=True)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, verbose_name='Public Identifier')

    inspection_interval = models.IntegerField('Inspection interval', null=False, blank=True)
    last_inspection_date = models.DateField('Last inspection', null=False, blank=True)
    next_inspection_date = None

    additional_information = models.TextField('Additional information', blank=True)

    def calc_inspection_date(self):
        self.next_inspection_date = self.last_inspection_date.day + self.inspection_interval * 7


"""
class Appointment(models.Model):
    create_datetime = models.DateTimeField('Creation date', auto_now_add=True, null=True)
    modified_datetime = models.DateTimeField('Last changes', null=True, blank=True, auto_now=True)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, verbose_name='Public Identifier')

    appointment_type = models.CharField(choices=APPOINTMENT_CHOICE)

    #replacement/maintenance/inspection
    appointment_interval = models.IntegerField('Maintenance interval', null=False, blank=True)
    last_appointment = models.DateField('Last maintenance', null=False, blank=True)
    next_appointment = None

    additional_information = models.TextField('Additional information', blank=True)

    def save(self, *args, **kwargs):
        self.next_appointment = self.appointment_interval * 7

        super(Inspection, self).save(*args, **kwargs)
 """


class Maintenance(models.Model):
    create_datetime = models.DateTimeField('Creation date', auto_now_add=True, null=True)
    modified_datetime = models.DateTimeField('Last changes', null=True, blank=True, auto_now=True)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, verbose_name='Public Identifier')

    maintenance_interval = models.IntegerField('Maintenance interval', null=False, blank=True)
    last_maintenance_date = models.DateField('Last maintenance', null=False, blank=True)
    next_maintenance_date = None

    additional_information = models.TextField('Additional information', blank=True)

    def calc_maintenance_date(self):
        self.next_maintenance_date = self.last_maintenance_date.day + self.maintenance_interval * 7


class Machinery(models.Model):
    create_datetime = models.DateTimeField('Creation date', auto_now_add=True, null=True)
    modified_datetime = models.DateTimeField('Last changes', null=True, blank=True, auto_now=True)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, verbose_name='Public Identifier')

    name = models.CharField('Name', max_length=150, null=False, blank=True)
    machinery_number = models.IntegerField('Machinery number', null=False, blank=False)
    machinery_type = models.ForeignKey(MachineryType, null=True, blank=False, on_delete=models.SET_NULL)

    date_of_installation = models.DateField('Date of installation', null=False, blank=True)

    inspection = models.ForeignKey('Inspection', Inspection, blank=False, null=False)

    maintenance = models.ForeignKey('Maintenance', Maintenance, blank=False, null=False)

    replacement_interval = models.IntegerField('Replacement time', null=False, blank=True)
    replacement_date = None

    location = models.ForeignKey('Location', Location, blank=False, null=False)
    company = models.ForeignKey('Company', Company, blank=False, null=False)

    def calc_replacement_date(self):
        self.replacement_date = self.date_of_installation.day + self.replacement_interval * 7


class Employee(models.Model):
    create_datetime = models.DateTimeField('Creation date', auto_now_add=True, null=True)
    modified_datetime = models.DateTimeField('Last changes', null=True, blank=True, auto_now=True)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, verbose_name='Public Identifier')

    last_name = models.CharField('Last name', max_length=150, blank=False, null=False)
    first_name = models.CharField('First name', max_length=150, blank=False, null=False)
    email = models.EmailField('E-Mail', max_length=150, blank=True)
    is_active = models.BooleanField(default=True)

    company = models.ForeignKey('Company', Company, blank=False, null=False)
    machinery = models.ManyToManyField(Machinery, blank=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    class Meta:
        permissions = (
        )


"""
    class Craft_Enterprise(models.Model):
    create_datetime = models.DateTimeField('Creation date', auto_now_add=True, null=True)
    modified_datetime = models.DateTimeField('Last changes', null=True, blank=True, auto_now=True)

    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, verbose_name='Public Identifier')

    name = models.CharField(max_length=500, blank=False, null=False, unique=True)
    email = models.EmailField('E-Mail', max_length=500, blank=True)
    strasse = models.CharField('Strasse', max_length=500, blank=True)
    hausnummer = models.CharField('Hausnummer', max_length=500, blank=True)
    plz = models.CharField('Postleitzahl', max_length=500, blank=True)
    stadt = models.CharField('Stadt', max_length=500, blank=False)
    land = models.CharField('Land', max_length=500, blank=True)

    def __str__(self):
        return self.name + ' [' + str(self.id) + ']'
"""
"""
class CompanyLocations(models.Model):
    create_datetime = models.DateTimeField('Creation date', auto_now_add=True, null=True)
    modified_datetime = models.DateTimeField('Last changes', null=True, blank=True, auto_now=True)

    company = models.ForeignKey('Company', Company, blank=False, null=False) #TODO Many to Many
    location = models.ForeignKey('Location', Location, blank=False, null=False)
"""

"""
class ResponsibleDevices(models.Model):
    create_datetime = models.DateTimeField('Creation date', auto_now_add=True, null=True)
    modified_datetime = models.DateTimeField('Last changes', null=True, blank=True, auto_now=True)

    employee = models.ForeignKey('Employee', Employee, blank=False, null=False)    #TODO Many to Many
    machinery = models.ForeignKey('Machinery', Machinery, blank=False, null=False)
"""
