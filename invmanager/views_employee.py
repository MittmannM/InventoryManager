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
def show_employee(request):
    #TODO get employee
    return render(request, "invmanager/employee.html")

#hallo
@login_required
def show_all_machinery(request):
    try:
        # TODO get employee
        machinery = Machinery.objects.filter()
    except (ValidationError):
        # TODO not registered namespace invmanager
        return HttpResponseRedirect((reverse('invmanager:company')))

    return render(request, "invmanager/list.html", {'list': machinery})

@login_required
def show_single_machinery(request, machinery_uuid):
    # TODO Zugriffsrechte einbauen
    # TODO wie bekommt man den Employee
    try:
        machinery = Machinery.objects.get(uuid=machinery_uuid)
    except (ObjectDoesNotExist, ValidationError):
        # TODO not registered namespace invmanager
        return HttpResponseRedirect((reverse('invmanager:company')))
    return render(request, "invmanager/unit.html", {'unit': machinery, })


@login_required
def show_all_appointments(request):
    try:
        # TODO fix next_date to be able to order correct
        # TODO get only the machines for the employee
        appointments1 = Inspection.objects.exclude().order_by('last_inspection_date')
        appointments2 = Maintenance.objects.exclude().order_by('last_maintenance_date')
        appointments = list(chain(appointments1, appointments2))

    except (ObjectDoesNotExist, ValidationError):
        # TODO not registered namespace invmanager
        return HttpResponseRedirect((reverse('invmanager:company')))
    return render(request, "invmanager/list.html", {'list': appointments, })
