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
def show_company(request):
    # TODO wie bekommt man die Company
    return render(request, "invmanager/company.html")


@login_required
def show_single_inventory(request, inventory_uuid):
    # TODO Zugriffsrechte einbauen
    # TODO wie bekommt man die Company
    try:
        inventory = Inventory.objects.get(uuid=inventory_uuid)
    except (ObjectDoesNotExist, ValidationError):
        # TODO not registered namespace invmanager
        return HttpResponseRedirect((reverse('invmanager:company')))
    return render(request, "invmanager/unit.html", {'unit': inventory})


@login_required
def show_all_inventory(request):
    # TODO Zugriffsrechte einbauen
    # TODO wie bekommt man die Company
    inventory = Inventory.objects.all()

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
        # TODO not registered namespace invmanager
        return HttpResponseRedirect((reverse('invmanager:company')))
    return render(request, "invmanager/unit.html", {'unit': machinery, })


@login_required
def show_all_employees(request):
    # TODO wie bekommt man die Company
    employees = Employee.objects.all().order_by('-last_name')

    return render(request, "invmanager/employee.html", {'employees': employees, })


@login_required
def show_all_employees_by_name(request, name):
    # TODO WIe bekommt man die Company

    employee = Employee.objects.exclude(last_name__contains=name)

    return render(request, "invmanager/employee.html", {'employees': employee})


@login_required
def show_single_employee_by_uuid(request, uuid):
    try:
        employee = Employee.objects.filter(uuid=uuid)
    except(ObjectDoesNotExist, ValidationError):
        # TODO not registered namespace invmanager
        return HttpResponseRedirect((reverse('invmanager:company')))
    return render(request, "invmanager/employee.html", {'employees': employee, })


@login_required
def show_all_employees_by_machine(request, machinery_uuid):
    try:
        employees = Employee.objects.filter(machinery__uuid=machinery_uuid)
    except(ObjectDoesNotExist, ValidationError):
        # TODO not registered namespace invmanager
        return HttpResponseRedirect((reverse('invmanager:company')))
    return render(request, "invmanager/employee.html", {'employees': employees})


@login_required
def show_all_machinery_by_employee(request, employee_uuid):

    try:
        machinery = Machinery.objects.filter(employee__uuid=employee_uuid)
    except(ObjectDoesNotExist, ValidationError):
        #TODO not registered namespace invmanager
        return HttpResponseRedirect((reverse('invmanager:company')))
    return render(request, "invmanager/list.html", {'list': machinery})


@login_required
def show_all_appointments(request):
    # TODO fix next_date to be able to order correct
    appointments1 = Inspection.objects.exclude().order_by('last_inspection_date')
    appointments2 = Maintenance.objects.exclude().order_by('last_maintenance_date')
    appointments = list(chain(appointments1, appointments2))

    return render(request, "invmanager/list.html", {'list': appointments, })

# TODO new functions for appointment search
