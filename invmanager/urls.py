from django.urls import path, include
from invmanager import views_employee

from . import views, views_company

app_name = 'invmanager'


urlpatterns = [
    path('', views.show_home, name='home'),

    path('abo', views.show_abo, name='show_subscription'),

    path('<company_uuid>/', include([
        path('', views_company.show_company, name='show_company'),
        # path('account', name='show_account'),
        path('employees', views_company.show_all_employees, name='show_all_employees'),
        path('employee/<employee_uuid>', views_company.show_single_employee_by_uuid, name='show_single_employee_by_uuid'),
        path('employees_<gadget_uuid>', views_company.show_all_employees_by_gadget, name='show_all_employees_by_gadget'),
        path('gadgets', views_company.show_all_gadgets, name='show_all_gadgets'),
        path('gadgets_<gadget_uuid>', views_company.show_single_gadget, name='show_single_gadget'),
        path('gadgets_<employee_uuid>/employees', views_company.show_all_gadgets_by_employee, name='show_all_gadgets_by_employee'),
        path('com_appointments', views_company.show_all_appointments, name='show_all_appointments'),
        path('com_appointments/<appointment_uuid>', views_company.show_single_appointment, name='show_single_appointment'),
        path('add_employee', views_company.add_employee, name='add_employee')
    ])),

    path('<employee_uuid>/', include([
        path('employee', views_employee.show_employee, name='show_employee'),
        # path('account', name='show_account'),
        path('machinery', views_employee.show_all_gadgets, name='show_all_gadgets'),
        path('machinery_<gadget_uuid>', views_employee.show_single_gadget, name='show_single_machine'),
        path('emp_appointments', views_employee.show_all_appointments, name='show_all_appointments'),
        path('emp_appointments/<appointment_uuid>', views_employee.show_single_appointment, name='show_single_appointment'),
    ])),

    path('no_object', views.no_object_exists, name='no_object_exists')

]
