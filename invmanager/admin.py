from django.contrib import admin
from invmanager.models import (
    Company,
    Employee,
    Inspection,
    Inventory,
    Location,
    MachineryType,
    Machinery,
    Maintenance,
)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'id',
        'uuid',

    )


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'uuid',
        'first_name',
        'last_name',


    )


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'uuid',
        'name',
        'product_number',
        'quantity',

    )


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'uuid',
        'city',
        'street',

    )


@admin.register(MachineryType)
class MachineryTypeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'uuid',
        'type',

    )


@admin.register(Machinery)
class MachineryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'uuid',
        'name',
        'machinery_number',
        'location',
        'company',

    )


@admin.register(Inspection)
class InspectionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'uuid',
        'last_inspection_date',
        'inspection_interval',
        'next_inspection_date'
    )


@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'uuid',
        'last_maintenance_date',
        'maintenance_interval',
        'next_maintenance_date',

    )
