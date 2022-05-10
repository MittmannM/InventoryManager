import requests
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
    #TODO wie bekommt man die Company
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

    try:
        inventory = Inventory.objects.filter()

    except (ValidationError):
        # TODO not registered namespace invmanager
        return HttpResponseRedirect((reverse('invmanager:company')))

    return render(request, "invmanager/list.html", {'list': inventory})


@login_required
def show_all_machinery(request):
    # TODO Zugriffsrechte einbauen
    # TODO wie bekommt man die Company
    try:
        machinery = Machinery.objects.filter()
    except (ValidationError):
        # TODO not registered namespace invmanager
        return HttpResponseRedirect((reverse('invmanager:company')))

    return render(request, "invmanager/list.html", {'list': machinery
                                                    })


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
    try:
        employees = Employee.objects.order_by('-last_name')

    except (ObjectDoesNotExist, ValidationError):
        # TODO not registered namespace invmanager
        return HttpResponseRedirect((reverse('invmanager:company')))
    return render(request, "invmanager/employee.html", {'employees': employees, })


@login_required
def show_all_appointments(request):
    try:
        # TODO fix next_date to be able to order correct
        appointments1 = Inspection.objects.exclude().order_by('last_inspection_date')
        appointments2 = Maintenance.objects.exclude().order_by('last_maintenance_date')
        appointments = list(chain(appointments1, appointments2))

    except (ObjectDoesNotExist, ValidationError):
        # TODO not registered namespace invmanager
        return HttpResponseRedirect((reverse('invmanager:company')))
    return render(request, "invmanager/list.html", {'list': appointments, })
