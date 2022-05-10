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

from django.core.exceptions import (
    ObjectDoesNotExist,
    MultipleObjectsReturned,
    ValidationError,
    )


def show_home(request):
    return render(request, "invmanager/home.html")


def show_abo(request):
    return render(request, "invmanager/abo.html")
