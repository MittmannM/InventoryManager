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


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'product_number',
        'quantity',
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


@admin.register(MachineryType)
class MachineryTypeAdmin(admin.ModelAdmin):
    list_display = (
        'type',
        'id',
        'uuid',
    )


@admin.register(Machinery)
class MachineryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'machinery_number',
        'machinery_type',
        'location',
        'company',
        'id',
        'uuid',
    )


@admin.register(Inspection)
class InspectionAdmin(admin.ModelAdmin):
    list_display = (
        'last_inspection_date',
        'inspection_interval',
        'next_inspection_date',
        'id',
        'uuid',
    )


@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):
    list_display = (
        'last_maintenance_date',
        'maintenance_interval',
        'next_maintenance_date',
        'id',
        'uuid',
    )
