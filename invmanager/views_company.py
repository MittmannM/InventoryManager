from itertools import chain
from .forms import EmployeeForm, GadgetTypeForm, GadgetForm, LocationForm, AppointmentForm


import requests
from django.shortcuts import (
    render,
    redirect,
    resolve_url
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

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Permission, User

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
        user = request.user
        if user != company.user:
            return render(request, "invmanager/access.html")
        company = Company.objects.get(uuid=company_uuid)
    except (ObjectDoesNotExist, ValidationError):
        return HttpResponseRedirect('no_object')
    return render(request, "invmanager/company.html", {'company': company})


@login_required
def show_all_gadgets(request, company_uuid):
    try:
        company = Company.objects.get(uuid=company_uuid)
        user = request.user
        if user != company.user:
            return render(request, "invmanager/access.html")
        gadgets = Gadget.objects.filter(company__uuid=company_uuid)
    except (ObjectDoesNotExist, ValidationError):
        return HttpResponseRedirect('no_object')
    return render(request, "invmanager/list.html", {'list': gadgets})


@login_required
def show_single_gadget(request, company_uuid, gadget_uuid):
    try:
        company = Company.objects.get(uuid=company_uuid)
        user = request.user
        if user != company.user:
            return render(request, "invmanager/access.html")
        gadget = Gadget.objects.get(company__uuid=company_uuid, uuid=gadget_uuid)
    except (ObjectDoesNotExist, ValidationError):
        return HttpResponseRedirect('no_object')
    return render(request, "invmanager/unit.html", {'unit': gadget, })


@login_required
def show_all_employees(request, company_uuid):
    try:
        company = Company.objects.get(uuid=company_uuid)
        user = request.user
        if user != company.user:
            return render(request, "invmanager/access.html")
        employees = Employee.objects.filter(company__uuid=company_uuid) \
            .order_by('-last_name')
    except (ObjectDoesNotExist, ValidationError):
        return HttpResponseRedirect('no_object')
    return render(request, "invmanager/employee.html", {'employees': employees, })


@login_required
def show_single_employee_by_uuid(request, company_uuid, employee_uuid):
    try:
        employee = Employee.objects.filter(company__uuid=company_uuid,
                                           uuid=employee_uuid)
        company = Company.objects.get(uuid=company_uuid)
        user = request.user
        if user != company.user:
            return render(request, "invmanager/access.html")
    except(ObjectDoesNotExist, ValidationError):
        return HttpResponseRedirect('no_object')
    return render(request, "invmanager/employee.html", {'employees': employee, })


@login_required
def show_all_employees_by_gadget(request, company_uuid, gadget_uuid):
    try:
        company = Company.objects.get(uuid=company_uuid)
        user = request.user
        if user != company.user:
            return render(request, "invmanager/access.html")

        employees = Employee.objects.filter(company__uuid=company_uuid,
                                            gadget__uuid=gadget_uuid)
    except(ObjectDoesNotExist, ValidationError):
        return HttpResponseRedirect('no_object')
    return render(request, "invmanager/employee.html", {'employees': employees})


@login_required
def show_all_gadgets_by_employee(request, company_uuid, employee_uuid):
    try:
        company = Company.objects.get(uuid=company_uuid)
        user = request.user
        if user != company.user:
            return render(request, "invmanager/access.html")
        gadgets = Gadget.objects.filter(company__uuid=company_uuid,
                                        employee__uuid=employee_uuid)
    except(ObjectDoesNotExist, ValidationError):
        return HttpResponseRedirect('no_object')
    return render(request, "invmanager/list.html", {'list': gadgets})


@login_required
def show_all_appointments(request, company_uuid):
    try:
        company = Company.objects.get(uuid=company_uuid)
        user = request.user
        if user != company.user:
            return render(request, "invmanager/access.html")
        appointments = Appointment.objects.filter(gadget__company__uuid=company_uuid).order_by("next_appointment")
    except(ObjectDoesNotExist, ValidationError):
        return HttpResponseRedirect('no_object')
    return render(request, "invmanager/list.html", {'list': appointments})


@login_required
def show_single_appointment(request, company_uuid, appointment_uuid):
    try:
        company = Company.objects.get(uuid=company_uuid)
        user = request.user
        if user != company.user:
            return render(request, "invmanager/access.html")
        appointment = Appointment.objects.get(gadget__company__uuid=company_uuid,
                                              uuid=appointment_uuid)
    except(ObjectDoesNotExist, ValidationError):
        return HttpResponseRedirect('no_object')
    return render(request, "invmanager/unit.html", {'unit': appointment})


@login_required
def add_employee(request, company_uuid):
    try:
        company = Company.objects.get(uuid=company_uuid)
        user = request.user
        if user != company.user:
            return render(request, "invmanager/access.html")

    except(ObjectDoesNotExist, ValidationError):
        return HttpResponseRedirect('no_object')

    if request.method == "POST":
        form = EmployeeForm(request.POST)

        if form.is_valid():
            form.save(commit=False)
            form.company = company.id
            form.save()
            return HttpResponseRedirect("/%i" % form.id)
    else:
        print("bruh")
        form = EmployeeForm()
    return render(request, "invmanager/add_employee.html", {"form": form})


@login_required
def add_gadget(request, company_uuid):
    try:
        company = Company.objects.get(uuid=company_uuid)
        user = request.user
        if user != company.user:
            return render(request, "invmanager/access.html")

    except(ObjectDoesNotExist, ValidationError):
        return HttpResponseRedirect('no_object')
    if request.method == "POST":
        form = GadgetForm(request.POST)

        if form.is_valid():
            form.save(commit=False)
            return HttpResponseRedirect(resolve_url("http://127.0.0.1:8000/" + company_uuid + "/add_gadget"))
    else:
        form = GadgetForm
    return render(request, "invmanager/add_gadget.html", {"form": form})


@login_required
def add_appointment(request, company_uuid):
    try:
        company = Company.objects.get(uuid=company_uuid)
        user = request.user
        if user != company.user:
            return render(request, "invmanager/access.html")

    except(ObjectDoesNotExist, ValidationError):
        return HttpResponseRedirect('no_object')
    if request.method == "POST":
        form = AppointmentForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(resolve_url("http://127.0.0.1:8000/" + company_uuid + "/add_appointment"))
    else:
        form = AppointmentForm()
    return render(request, "invmanager/add_appointment.html", {"form": form})


@login_required
def add_location(request, company_uuid):
    try:
        company = Company.objects.get(uuid=company_uuid)
        user = request.user
        if user != company.user:
            return render(request, "invmanager/access.html")

    except(ObjectDoesNotExist, ValidationError):
        return HttpResponseRedirect('no_object')
    if request.method == "POST":
        form = LocationForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(resolve_url("http://127.0.0.1:8000/" + company_uuid + "/add_location"))
    else:
        form = LocationForm()
    return render(request, "invmanager/add_location.html", {"form": form})


@login_required
def add_gadget_type(request, company_uuid):
    try:
        company = Company.objects.get(uuid=company_uuid)
        user = request.user
        if user != company.user:
            return render(request, "invmanager/access.html")

    except(ObjectDoesNotExist, ValidationError):
        return HttpResponseRedirect('no_object')
    if request.method == "POST":
        form = GadgetTypeForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(resolve_url("http://127.0.0.1:8000/" + company_uuid + "/add_gadgettype"))
    else:
        form = GadgetTypeForm()
    return render(request, "invmanager/add_gadget_type.html", {"form": form})


@login_required
def update_gadget_type(request, company_uuid, gadgettype_uuid):
    try:
        company = Company.objects.get(uuid=company_uuid)
        user = request.user
        if user != company.user:
            return render(request, "invmanager/access.html")
        gadget_type = GadgetType.objects.get(uuid=gadgettype_uuid) #TODO Sicherheitslücke
        form = GadgetTypeForm(instance=gadget_type)
    except(ObjectDoesNotExist, ValidationError):
        return HttpResponseRedirect('no_object')

    if request.method == 'POST':
        form = GadgetTypeForm(request.POST, instance=gadget_type)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(resolve_url("http://127.0.0.1:8000/" + company_uuid + "/addGadgetType"))
    return render(request, 'invmanager/add_gadget_type.html', {"form": form})


@login_required
def update_gadget(request, company_uuid, gadget_uuid):
    try:
        company = Company.objects.get(uuid=company_uuid)
        user = request.user
        if user != company.user:
            return render(request, "invmanager/access.html")
        gadget = Gadget.objects.get(uuid=gadget_uuid)
        if gadget.company != company:
            return HttpResponse('this gadget could not be found within your company')
        form = GadgetForm(instance=gadget)
    except(ObjectDoesNotExist, ValidationError):
        return HttpResponseRedirect('no_object')

    if request.method == 'POST':
        form = GadgetForm(request.POST, instance=gadget)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(resolve_url("http://127.0.0.1:8000/" + company_uuid + "/addGadget"))
    return render(request, 'invmanager/add_gadget.html', {"form": form})


@login_required
def update_location(request, company_uuid, location_uuid):
    try:
        company = Company.objects.get(uuid=company_uuid)
        user = request.user
        if user != company.user:
            return render(request, "invmanager/access.html")
        location = Location.objects.get(uuid=location_uuid) #TODO Sicherheitslücke
        form = LocationForm(instance=location)
    except(ObjectDoesNotExist, ValidationError):
        return HttpResponseRedirect('no_object')

    if request.method == 'POST':
        form = LocationForm(request.POST, instance=location)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(resolve_url("http://127.0.0.1:8000/" + company_uuid + "/addLocation"))
    return render(request, 'invmanager/add_location.html', {"form": form})


@login_required
def update_appointment(request, company_uuid, appointment_uuid):
    try:
        company = Company.objects.get(uuid=company_uuid)
        user = request.user
        if user != company.user:
            return render(request, "invmanager/access.html")
        appointment = Appointment.objects.get(uuid=appointment_uuid) #TODO Sicherheitslücke
        form = AppointmentForm(instance=appointment)
    except(ObjectDoesNotExist, ValidationError):
        return HttpResponseRedirect('no_object')

    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(resolve_url("http://127.0.0.1:8000/" + company_uuid + "/addAppointment"))
    return render(request, 'invmanager/add_appointment.html', {"form": form})


@login_required
def update_employee(request, company_uuid, employee_uuid):
    try:
        company = Company.objects.get(uuid=company_uuid)
        user = request.user
        if user != company.user:
            return render(request, "invmanager/access.html")
        employee = Employee.objects.get(uuid=employee_uuid) #TODO Sicherheitslücke
        form = AppointmentForm(instance=employee)
    except(ObjectDoesNotExist, ValidationError):
        return HttpResponseRedirect('no_object')
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(resolve_url("http://127.0.0.1:8000/" + company_uuid + "/addEmployee"))
    return render(request, 'invmanager/add_employee.html', {"form": form})


@login_required
def delete_employee(request, company_uuid, employee_uuid):
    try:
        company = Company.objects.get(uuid=company_uuid)
        user = request.user
        if user != company.user:
            return render(request, "invmanager/access.html")
        print("geht noch")
        employee = Employee.objects.get(uuid=employee_uuid)
        print("auch noch")
    except(ObjectDoesNotExist, ValidationError):
        return HttpResponse('no_object')
    if request.method == "POST":
        employee.delete()
        return HttpResponse("invmanager/home.html")
    return render(request, 'invmanager/delete.html', {'item': employee,
                                                      'company': company})
