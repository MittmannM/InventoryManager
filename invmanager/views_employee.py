
from itertools import chain

from django.shortcuts import (
    render,
    redirect
)

from .models import (
    Appointment,
    Company,
    Employee,
    Location,
    Gadget,
    GadgetType,
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
def show_employee(request, employee_uuid):
    # TODO Zugriffsrechte einbauen
    try:
        employee = Employee.objects.get(uuid=employee_uuid)
    except (ObjectDoesNotExist, ValidationError):
        return HttpResponseRedirect('no_object')
    return render(request, "invmanager/unit.html", {'unit': employee})


@login_required
def show_all_gadgets(request, employee_uuid):
    # TODO Zugriffsrechte einbauen
    gadgets = Gadget.objects.filter(employee__uuid=employee_uuid)
    return render(request, "invmanager/list.html", {'list': gadgets})


@login_required
def show_single_gadget(request, gadget_uuid, employee_uuid):
    # TODO Zugriffsrechte einbauen
    try:
        gadget = Gadget.objects.get(uuid=gadget_uuid,
                                    employee__uuid=employee_uuid)
    except (ObjectDoesNotExist, ValidationError):
        return HttpResponseRedirect('no_object')
    return render(request, "invmanager/unit.html", {'unit': gadget, })


@login_required
def show_all_appointments(request, employee_uuid):
    # TODO Zugriffsrechte einbauen
    appointments = Appointment.objects.filter(gadget__employee__uuid=employee_uuid)

        # TODO fix next_date to be able to order correct

    return render(request, "invmanager/list.html", {'list': appointments,})


@login_required
def show_single_appointment(request, employee_uuid, appointment_uuid):
    # TODO only user can see
    try:
        appointment = Appointment.objects.get(gadget__employee__uuid=employee_uuid,
                                              uuid=appointment_uuid)
    except(ObjectDoesNotExist, ValidationError):
        return HttpResponseRedirect('no_object')
    return render(request, "invmanager/unit.html", {'unit': appointment})
