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
        path('add_employee', views_company.add_employee, name='add_employee'),
        path('add_gadgettype', views_company.add_gadget_type, name='add_gadgettype'),
        path('add_location', views_company.add_location, name='add_location'),
        path('add_appointment', views_company.add_appointment, name='add_appointment'),
        path('add_gadget', views_company.add_gadget, name='add_gadget'),
        path('update_gagdget_type/<gadgettype_uuid>', views_company.update_gadget_type, name='update_gadget_type'),
        path('update_gadget/<gadget_uuid>', views_company.update_gadget, name='update_gadget'),
        path('update_appointment/<appointment_uuid>', views_company.update_appointment, name='update_appointment'),
        path('update_location/<location_uuid>', views_company.update_location, name='update_location'),
        path('update_employee/<employee_uuid>', views_company.update_employee, name='update_employee'),
        path('delete_employee/<employee_uuid>', views_company.delete_employee, name='delete_employee'),
        path('delete_appointment/<appointment_uuid>', views_company.delete_appointment, name='delete_appointment'),
        path('delete_location/<location_uuid>', views_company.delete_location, name='delete_location'),
        path('delete_gadget/<gadget_uuid>', views_company.delete_gadget, name='delete_gadget'),
        path('delete_gadget_type/<gadgettype_uuid>', views_company.delete_gadget_type, name='delete_gadget_type'),
    ])),

    path('<employee_uuid>/', include([
        path('employee', views_employee.show_employee, name='show_employee'),
        # path('account', name='show_account'),
        path('machinery', views_employee.show_all_gadgets, name='show_all_gadgets'),
        path('machinery_<gadget_uuid>', views_employee.show_single_gadget, name='show_single_machine'),
        path('emp_appointments', views_employee.show_all_appointments, name='show_all_appointments'),
        path('emp_appointments/<appointment_uuid>', views_employee.show_single_appointment, name='show_single_appointment'),
        path('addGadgetType', views_employee.create_gadget_type, name='add_gadgettype'),
        path('addLocation', views_employee.create_location, name='add_location'),
        path('addAppointment', views_employee.create_appointment, name='add_appointment'),
        path('addGadget', views_employee.create_gadget, name='add_gadget'),
        path('updateGadgetType/<gadgettype_uuid>', views_employee.update_gadget_type, name='update_gadget_type'),
        path('updateGadget/<gadget_uuid>', views_employee.update_gadget, name='update_gadget'),
        path('updateLocation/<location_uuid>', views_employee.update_location, name='update_location'),
        path('updateAppointment/<appointment_uuid>', views_employee.update_appointment, name='update_appointment'),
        path('deleteAppointment/<appointment_uuid>', views_employee.delete_appointment, name='deleteAppointment'),
        path('deleteLocation/<location_uuid>', views_employee.delete_location, name='deleteLocation'),
        path('deleteGadget/<gadget_uuid>', views_employee.delete_gadget, name='deleteGadget'),
        path('deleteGadgetType/<gadgettype_uuid>', views_employee.delete_gadget_type, name='deleteGadgetType'),
    ])),

    path('no_object', views.no_object_exists, name='no_object_exists'),

]
