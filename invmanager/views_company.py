from itertools import chain

from django.shortcuts import (
    render,
    redirect
)

from .models import (
    Company,
    Employee,
    Inspection,
    Inventory,
    Location,
    Machinery,
    MachineryType,
    Maintenance,
)
from django.http import (
    HttpResponse,
    HttpResponseNotFound,
    HttpResponseRedirect
)

from django.core.paginator import Paginator

from django.contrib.auth.decorators import login_required

from django.urls import reverse

from django.core.exceptions import (
    ObjectDoesNotExist,
    MultipleObjectsReturned,
    ValidationError,
)


@login_required
def show_company(request, company_uuid):
    try:
        company = Company.objects.get(uuid=company_uuid)
    except (ObjectDoesNotExist, ValidationError):
        return HttpResponseRedirect('no_object')
    return render(request, "invmanager/company.html", {'company': company})


@login_required
def show_single_inventory(request, company_uuid, inventory_uuid):
    # TODO Zugriffsrechte einbauen
    try:
        inventory = Inventory.objects.get(company__uuid=company_uuid,
                                          uuid=inventory_uuid)
    except (ObjectDoesNotExist, ValidationError):
        return HttpResponseRedirect('no_object')
    return render(request, "invmanager/unit.html", {'unit': inventory})


@login_required
def show_all_inventory(request, company_uuid):
    # TODO Zugriffsrechte einbauen
    inventory = Inventory.objects.filter(company__uuid=company_uuid).order_by('name', 'quantity')
    return render(request, "invmanager/list.html", {'list': inventory})


@login_required
def show_all_machinery(request):
    # TODO Zugriffsrechte einbauen
    # TODO wie bekommt man die Company
    machinery = Machinery.objects.all()

    return render(request, "invmanager/list.html", {'list': machinery})


@login_required
def show_single_machinery(request, machinery_uuid):
    # TODO Zugriffsrechte einbauen
    # TODO wie bekommt man die Company
    try:
        machinery = Machinery.objects.get(uuid=machinery_uuid)
    except (ObjectDoesNotExist, ValidationError):
        return HttpResponseRedirect('no_object')
    return render(request, "invmanager/unit.html", {'unit': machinery, })


@login_required
def show_all_employees(request, company_uuid):
    employees = Employee.objects.filter(company__uuid=company_uuid).order_by('-last_name')

    return render(request, "invmanager/employee.html", {'employees': employees, })


@login_required
def show_all_employees_by_name(request, company_uuid, name):
    employee = Employee.objects \
        .filter(company__uuid=company_uuid,
                last_name=name)

    return render(request, "invmanager/employee.html", {'employees': employee})


@login_required
def show_single_employee_by_uuid(request, company_uuid, uuid):
    try:
        employee = Employee.objects.filter(company__uuid=company_uuid,
                                           uuid=uuid)
    except(ObjectDoesNotExist, ValidationError):
        return HttpResponseRedirect('no_object')
    return render(request, "invmanager/employee.html", {'employees': employee, })


@login_required
def show_all_employees_by_machine(request, company_uuid, machinery_uuid):
    try:
        employees = Employee.objects.filter(company__uuid=company_uuid,
                                            machinery__uuid=machinery_uuid)
    except(ObjectDoesNotExist, ValidationError):
        return HttpResponseRedirect('no_object')
    return render(request, "invmanager/employee.html", {'employees': employees})


@login_required
def show_all_machinery_by_employee(request, company_uuid, employee_uuid):
    try:
        machinery = Machinery.objects.filter(company__uuid=company_uuid,
                                             employee__uuid=employee_uuid)
    except(ObjectDoesNotExist, ValidationError):
        return HttpResponseRedirect('no_object')
    return render(request, "invmanager/list.html", {'list': machinery})


@login_required
def show_all_appointments(request):
    # TODO fix next_date to be able to order correct
    appointments1 = Inspection.objects.exclude().order_by('last_inspection_date')
    appointments2 = Maintenance.objects.exclude().order_by('last_maintenance_date')
    appointments = list(chain(appointments1, appointments2))

    return render(request, "invmanager/list.html", {'list': appointments, })

# TODO new functions for appointment search
