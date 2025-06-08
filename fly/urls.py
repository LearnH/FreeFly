
from django.urls import path
from fly.views import dashboard, operating_base, airport, employee
from fly.views.organization import company, department, position


urlpatterns = [
    path('index/', dashboard.dashboard, name='dashboard'),
    path('operating_base/', operating_base.operating_base, name='operating_base'),
    path('operating_base/add/', operating_base.operating_base_add, name='operating_base_add'),
    path('operating_base/<int:nid>/edit/', operating_base.operating_base_edit, name='operating_base_edit'),
    path('operating_base/<int:nid>/delete/', operating_base.operating_base_delete, name='operating_base_delete'),
    path('airport/', airport.airport, name='airport'),
    path('airport/add/', airport.airport_add, name='airport_add'),
    path('airport/<int:nid>/edit/', airport.airport_edit, name='airport_edit'),
    path('airport/<int:nid>/delete/', airport.airport_delete, name='airport_delete'),
    path('employee/', employee.employee, name='employee'),
    path('employee/add/', employee.employee_add, name='employee_add'),
    path('employee/<int:nid>/edit/', employee.employee_edit, name='employee_edit'),
    path('employee/<int:nid>/delete/', employee.employee_delete, name='employee_delete'),
    path('department/', department.department, name='department'),
    path('department/add/', department.department_add, name='department_add'),
    path('department/<int:nid>/edit/', department.department_edit, name='department_edit'),
    path('department/<int:nid>/delete/', department.department_delete, name='department_delete'),
    path('company/', company.company, name='company'),
    path('company/add/', company.company_add, name='company_add'),
    path('company/<int:nid>/edit/', company.company_edit, name='company_edit'),
    path('company/<int:nid>/delete/', company.company_delete, name='company_delete'),
    path('position/', position.position, name='position'),
    path('position/add/', position.position_add, name='position_add'),
    path('position/<int:nid>/edit/', position.position_edit, name='position_edit'),
    path('position/<int:nid>/delete/', position.position_delete, name='position_delete'),
]
