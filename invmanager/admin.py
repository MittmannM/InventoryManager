from django.contrib import admin
from invmanager.models import (
    Appointment,
    Company,
    Employee,
    Location,
    Gadget,
    GadgetType,
)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'is_craft_enterprise',
        'id',
        'uuid',

    )


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        'last_name',
        'first_name',
        'company',
        'id',
        'uuid',
    )


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'country',
        'city',
        'street',
        'id',
        'uuid',
    )


@admin.register(GadgetType)
class GadgetTypeAdmin(admin.ModelAdmin):
    list_display = (
        'type',
        'id',
        'uuid',
    )


@admin.register(Gadget)
class GadgetAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'number',
        'type',
        'location',
        'company',
        'id',
        'uuid',
    )


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        'type',
        'interval',
        'last_appointment',
        'next_appointment',
        'uuid',
    )
