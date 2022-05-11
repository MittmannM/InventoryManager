from django.urls import path, include
from invmanager import views_employee

from . import views, views_company

app_name = 'invmanager'

# TODO funktionen mit einfachem template html 'save html'

urlpatterns = [
    path('', views.show_home, name='home'),

    path('abo', views.show_abo, name='show_subscription'),

    # TODO Maybe <company> ?
    path('company/', include([
        path('', views_company.show_company, name='show_company'),
        # path('account', name='show_account'),
        path('employees', views_company.show_all_employees, name='show_all_employees'),
        path('employee_<name>', views_company.show_single_employee_by_name, name='show_single_employee_by_name'),
        path('inventories', views_company.show_all_inventory, name='show_all_inventories'),
        path('inventory_<inventory_uuid>', views_company.show_single_inventory, name='show_single_inventory'),
        path('machinery', views_company.show_all_machinery, name='show_all_machinery'),
        path('machinery_<machinery_uuid>', views_company.show_single_machinery, name='show_single_machine'),
        path('appointments', views_company.show_all_appointments, name='show_appointments')
    ])),

    path('employee/', include([
        path('', views_employee.show_employee, name='show_employee'),
        # path('account', name='show_account'),
        path('machinery', views_employee.show_all_machinery, name='show_all_machinery'),
        path('machinery_<machinery_uuid>', views_employee.show_single_machinery, name='show_single_machine'),
        path('appointments', views_employee.show_all_appointments, name='show_appointments')
    ])),

]
