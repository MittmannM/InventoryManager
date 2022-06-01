from itertools import chain
from .forms import AddEmployee, AddGadget, AddGadgetType, AddLocation, AddAppointment

import requests
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
    if request.method == "POST":
        form = AddEmployee(request.POST)

        if form.is_valid():
            fn = form.cleaned_data["first_name"]
            ln = form.cleaned_data["last_name"]
            e = form.cleaned_data["email"]
            t = Employee(first_name=fn, last_name=ln, email=e)
            t.save()
            return HttpResponseRedirect("/%i" % t.id)
    else:
        form = AddEmployee()
    return render(request, "invmanager/add_employee.html", {"form": form})


@login_required
def add_gadget(request, company_uuid):
    if request.method == "POST":
        form = AddGadget(request.POST)

        if form.is_valid():
            n = form.cleaned_data["name"]
            num = form.cleaned_data["number"]
            image = form.cleaned_data["image"]
            insdate = form.cleaned_data["installation_date"]
            t = Gadget(name=n,number=num,image=image,date_of_installation=insdate)
            t.save()
            return HttpResponseRedirect("/%i" % t.id)
    else:
        form = AddGadget()
    return render(request, "invmanager/add_gadget.html", {"form": form})


@login_required
def add_appointment(request, company_uuid):
    if request.method == "POST":
        form = AddAppointment(request.POST)

        if form.is_valid():
            type = form.cleaned_data["type"]
            interval = form.cleaned_data["interval"]
            la = form.cleaned_data["last_appointment"]
            na = form.cleaned_data["next_appointment"]
            ai = form.cleaned_data["additional_information"]
            t = Appointment(type=type,interval = interval,last_appointment=la,next_appointment=na,additional_information=ai)
            t.save()
            return HttpResponseRedirect("/%i" % t.id)
    else:
        form = AddAppointment()
    return render(request, "invmanager/add_appointment.html", {"form": form})


@login_required
def add_location(request, company_uuid):
    if request.method == "POST":
        form = AddLocation(request.POST)

        if form.is_valid():
            str = form.cleaned_data["street"]
            hn = form.cleaned_data["house_number"]
            pc = form.cleaned_data["postal_code"]
            city = form.cleaned_data["city"]
            country = form.cleaned_data["country"]
            t = Location(street=str,house_number=hn,postal_code=pc,city=city,country=country)
            t.save()
            return HttpResponseRedirect("/%i" % t.id)
    else:
        form = AddLocation()
    return render(request, "invmanager/add_location.html", {"form": form})


@login_required
def add_gadget_type(request, company_uuid):
    if request.method == "POST":
        form = AddGadgetType(request.POST)

        if form.is_valid():
            type = form.cleaned_data["type"]
            t = GadgetType(type=type)
            t.save()
            return HttpResponseRedirect("/%i" % t.id)
    else:
        form = AddGadgetType()
    return render(request, "invmanager/add_gadget_type.html", {"form": form})
