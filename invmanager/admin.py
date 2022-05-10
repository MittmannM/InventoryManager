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
        'id',
        'uuid',
        'create_datetime',
        'modified_datetime',
    )


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'uuid',
        'create_datetime',
        'modified_datetime',

    )


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'uuid',
        'create_datetime',
        'modified_datetime',

    )


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'uuid',
        'create_datetime',
        'modified_datetime',

    )


@admin.register(MachineryType)
class MachineryTypeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'uuid',
        'create_datetime',
        'modified_datetime',

    )


@admin.register(Machinery)
class MachineryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'uuid',
        'create_datetime',
        'modified_datetime',

    )

@admin.register(Inspection)
class InspectionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'uuid',
        'create_datetime',
        'modified_datetime',
        'next_inspection_date'
    )

@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'uuid',
        'create_datetime',
        'modified_datetime',
    )