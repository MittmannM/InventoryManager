from .forms import GadgetTypeForm, GadgetForm, LocationForm, AppointmentForm

from django.shortcuts import (
    render,
    redirect,
    resolve_url,
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
    try:
        employee = Employee.objects.get(uuid=employee_uuid)
        user = request.user
        if user != employee.user:
            return render(request, "invmanager/access.html")
        employee = Employee.objects.get(uuid=employee_uuid)
    except (ObjectDoesNotExist, ValidationError):
        return HttpResponseRedirect('no_object')
    return render(request, "invmanager/unit.html", {'unit': employee})


@login_required
def show_all_gadgets(request, employee_uuid):
    try:
        employee = Employee.objects.get(uuid=employee_uuid)
        user = request.user
        if user != employee.user:
            return render(request, "invmanager/access.html")
        gadgets = Gadget.objects.filter(employee__uuid=employee_uuid)
    except (ObjectDoesNotExist, ValidationError):
        return HttpResponseRedirect('no_object')
    return render(request, "invmanager/list.html", {'list': gadgets})


@login_required
def show_single_gadget(request, gadget_uuid, employee_uuid):
    try:
        employee = Employee.objects.get(uuid=employee_uuid)
        user = request.user
        if user != employee.user:
            return render(request, "invmanager/access.html")
        gadget = Gadget.objects.get(uuid=gadget_uuid,
                                    employee__uuid=employee_uuid)
    except (ObjectDoesNotExist, ValidationError):
        return HttpResponseRedirect('no_object')
    return render(request, "invmanager/unit.html", {'unit': gadget, })


@login_required
def show_all_appointments(request, employee_uuid):
    try:
        employee = Employee.objects.get(uuid=employee_uuid)
        user = request.user
        if user != employee.user:
            return render(request, "invmanager/access.html")
        appointments = Appointment.objects.filter(gadget__employee__uuid=employee_uuid).order_by("next_appointment")
    except (ObjectDoesNotExist, ValidationError):
        return HttpResponseRedirect('no_object')
    return render(request, "invmanager/list.html", {'list': appointments, })


@login_required
def show_single_appointment(request, employee_uuid, appointment_uuid):
    try:
        employee = Employee.objects.get(uuid=employee_uuid)
        user = request.user
        if user != employee.user:
            return render(request, "invmanager/access.html")
        appointment = Appointment.objects.get(gadget__employee__uuid=employee_uuid,
                                              uuid=appointment_uuid)
    except(ObjectDoesNotExist, ValidationError):
        return HttpResponseRedirect('no_object')
    return render(request, "invmanager/unit.html", {'unit': appointment})


@login_required
def create_gadget(request, employee_uuid):
    try:
        employee = Employee.objects.get(uuid=employee_uuid)
        user = request.user
        if user != employee.user:
            return render(request, "invmanager/access.html")

    except(ObjectDoesNotExist, ValidationError):
        return HttpResponseRedirect('no_object')
    if request.method == "POST":
        form = GadgetForm(request.POST)

        if form.is_valid():
            form.save(commit=False)
            return HttpResponseRedirect(resolve_url("http://127.0.0.1:8000/" + employee_uuid + "/addGadget"))
    else:
        form = GadgetForm()
    return render(request, "invmanager/add_gadget.html", {"form": form})


@login_required
def create_appointment(request, employee_uuid):
    try:
        employee = Employee.objects.get(uuid=employee_uuid)
        user = request.user
        if user != employee.user:
            return render(request, "invmanager/access.html")

    except(ObjectDoesNotExist, ValidationError):
        return HttpResponseRedirect('no_object')
    if request.method == "POST":
        form = AppointmentForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(resolve_url("http://127.0.0.1:8000/" + employee_uuid + "/addAppointment"))
    else:
        form = AppointmentForm()
    return render(request, "invmanager/add_appointment.html", {"form": form})


@login_required
def create_location(request, employee_uuid):
    try:
        employee = Employee.objects.get(uuid=employee_uuid)
        user = request.user
        if user != employee.user:
            return render(request, "invmanager/access.html")

    except(ObjectDoesNotExist, ValidationError):
        return HttpResponseRedirect('no_object')
    if request.method == "POST":
        form = LocationForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(resolve_url("http://127.0.0.1:8000/" + employee_uuid + "/addLocation"))
    else:
        form = LocationForm()
    return render(request, "invmanager/add_location.html", {"form": form})


@login_required
def create_gadget_type(request, employee_uuid):
    try:
        employee = Employee.objects.get(uuid=employee_uuid)
        user = request.user
        if user != employee.user:
            return render(request, "invmanager/access.html")

    except(ObjectDoesNotExist, ValidationError):
        return HttpResponseRedirect('no_object')
    if request.method == "POST":
        form = GadgetTypeForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(resolve_url("http://127.0.0.1:8000/" + employee_uuid + "/addGadgetType"))
    else:
        form = GadgetTypeForm()
    return render(request, "invmanager/add_gadget_type.html", {"form": form})


@login_required
def update_gadget_type(request, employee_uuid, gadgettype_uuid):
    try:
        employee = Employee.objects.get(uuid=employee_uuid)
        user = request.user
        if user != employee.user:
            return render(request, "invmanager/access.html")
        gadget_type = GadgetType.objects.get(uuid=gadgettype_uuid)  # TODO Sicherheitslücke
        form = GadgetTypeForm(instance=gadget_type)
    except(ObjectDoesNotExist, ValidationError):
        return HttpResponseRedirect('no_object')

    if request.method == 'POST':
        form = GadgetTypeForm(request.POST, instance=gadget_type)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(resolve_url("http://127.0.0.1:8000/" + employee_uuid + "/addGadgetType"))
    return render(request, 'invmanager/add_gadget_type.html', {"form": form})


@login_required
def update_gadget(request, employee_uuid, gadget_uuid):
    try:
        employee = Employee.objects.get(uuid=employee_uuid)
        user = request.user
        if user != employee.user:
            return render(request, "invmanager/access.html")
        gadget = Gadget.objects.get(uuid=gadget_uuid)
        if gadget.company != employee.company:
            return HttpResponse('this gadget could not be found within your company')
        form = GadgetForm(instance=gadget)
    except(ObjectDoesNotExist, ValidationError):
        return HttpResponseRedirect('no_object')

    if request.method == 'POST':
        form = GadgetForm(request.POST, instance=gadget)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(resolve_url("http://127.0.0.1:8000/" + employee_uuid + "/addGadget"))
    return render(request, 'invmanager/add_gadget.html', {"form": form})


@login_required
def update_location(request, employee_uuid, location_uuid):
    try:
        employee = Employee.objects.get(uuid=employee_uuid)
        user = request.user
        if user != employee.user:
            return render(request, "invmanager/access.html")
        location = Location.objects.get(uuid=location_uuid)  # TODO Sicherheitslücke
        form = LocationForm(instance=location)
    except(ObjectDoesNotExist, ValidationError):
        return HttpResponseRedirect('no_object')

    if request.method == 'POST':
        form = LocationForm(request.POST, instance=location)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(resolve_url("http://127.0.0.1:8000/" + employee_uuid + "/addLocation"))
    return render(request, 'invmanager/add_location.html', {"form": form})


@login_required
def update_appointment(request, employee_uuid, appointment_uuid):
    try:
        employee = Employee.objects.get(uuid=employee_uuid)
        user = request.user
        if user != employee.user:
            return render(request, "invmanager/access.html")
        appointment = Appointment.objects.get(uuid=appointment_uuid)  # TODO Sicherheitslücke
        form = AppointmentForm(instance=appointment)
    except(ObjectDoesNotExist, ValidationError):
        return HttpResponseRedirect('no_object')

    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(resolve_url("http://127.0.0.1:8000/" + employee_uuid + "/addAppointment"))
    return render(request, 'invmanager/add_appointment.html', {"form": form})


@login_required
def delete_location(request, location_uuid, employee_uuid):
    try:
        employee = Employee.objects.get(uuid=employee_uuid)
        user = request.user
        if user != employee.user:
            return render(request, "invmanager/access.html")
        location = Location.objects.get(uuid=location_uuid)
    except(ObjectDoesNotExist, ValidationError):
        return HttpResponse('no_object')

    if request.method == "POST":
        location.delete()
        return HttpResponse("invmanager/home.html")
    return render(request, 'invmanager/delete.html', {'item': location,
                                                      'company': employee})


@login_required
def delete_gadget(request, gadget_uuid, employee_uuid):
    try:
        employee = Employee.objects.get(uuid=employee_uuid)
        user = request.user
        if user != employee.user:
            return render(request, "invmanager/access.html")
        gadget = Gadget.objects.get(uuid=gadget_uuid)
    except(ObjectDoesNotExist, ValidationError):
        return HttpResponse('no_object')

    if request.method == "POST":
        gadget.delete()
        return HttpResponse("invmanager/home.html")
    return render(request, 'invmanager/delete.html', {'item': gadget,
                                                      'company': employee})


@login_required
def delete_gadget_type(request, gadgettype_uuid, employee_uuid):
    try:
        employee = Employee.objects.get(uuid=employee_uuid)
        user = request.user
        if user != employee.user:
            return render(request, "invmanager/access.html")
        gadget_type = GadgetType.objects.get(uuid=gadgettype_uuid)
    except(ObjectDoesNotExist, ValidationError):
        return HttpResponse('no_object')

    if request.method == "POST":
        gadget_type.delete()
        return HttpResponse("invmanager/home.html")
    return render(request, 'invmanager/delete.html', {'item': gadget_type,
                                                      'company': employee})


@login_required
def delete_appointment(request, appointment_uuid, employee_uuid):
    try:
        employee = Employee.objects.get(uuid=employee_uuid)
        user = request.user
        if user != employee.user:
            return render(request, "invmanager/access.html")
        appointment = Appointment.objects.get(uuid=appointment_uuid)
    except(ObjectDoesNotExist, ValidationError):
        return HttpResponse('no_object')

    if request.method == "POST":
        appointment.delete()
        return HttpResponse("invmanager/home.html")
    return render(request, 'invmanager/delete.html', {'item': appointment,
                                                      'company': employee})
