from itertools import chain
from .forms import AddEmployee

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
        employees = Employee.objects.filter(company__uuid=company_uuid)\
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
    form = AddEmployee()
    return render(request, "invmanager/add_employee.html", {"form": form})
