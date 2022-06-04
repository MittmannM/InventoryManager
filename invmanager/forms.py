from django.forms import ModelForm
from .models import Employee, Gadget, GadgetType, Appointment, Location


class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = ['last_name',
                  'first_name',
                  'email',
                  'is_active',
                  'gadget']


class GadgetForm(ModelForm):
    class Meta:
        model = Gadget
        fields = ['name',
                  'number',
                  'type',
                  'image',
                  'date_of_installation',
                  'appointments',
                  'location']


class GadgetTypeForm(ModelForm):
    class Meta:
        model = GadgetType
        fields = ['type']


class LocationForm(ModelForm):
    class Meta:
        model = Location
        fields = ['street',
                  'house_number',
                  'postal_code',
                  'city',
                  'country']


class AppointmentForm(ModelForm):
    class Meta:
        model = Appointment
        fields = ['type',
                  'interval',
                  'next_appointment',
                  'last_appointment',
                  'additional_information']
