
from django.urls import path
from fly.views import dashboard, employee, student, flight_course, flight_record, admin, custom_auth
from fly.views.organization import company, department, position
from fly.views.basic_archives import aircraft_type, aircraft, airport, operating_base

urlpatterns = [
    path('index/', dashboard.dashboard, name='dashboard'),

    # 基地
    path('operating_base/', operating_base.operating_base, name='operating_base'),
    path('operating_base/add/', operating_base.operating_base_add, name='operating_base_add'),
    path('operating_base/<int:nid>/edit/', operating_base.operating_base_edit, name='operating_base_edit'),
    path('operating_base/<int:nid>/delete/', operating_base.operating_base_delete, name='operating_base_delete'),

    # 机场
    path('airport/', airport.airport, name='airport'),
    path('airport/add/', airport.airport_add, name='airport_add'),
    path('airport/<int:nid>/edit/', airport.airport_edit, name='airport_edit'),
    path('airport/<int:nid>/delete/', airport.airport_delete, name='airport_delete'),

    # 员工
    path('employee/', employee.employee, name='employee'),
    path('employee/add/', employee.employee_add, name='employee_add'),
    path('employee/<int:nid>/edit/', employee.employee_edit, name='employee_edit'),
    path('employee/<int:nid>/delete/', employee.employee_delete, name='employee_delete'),

    # 学生
    path('student/', student.student, name='student'),
    path('student/add/', student.student_add, name='student_add'),
    path('student/<int:nid>/edit/', student.student_edit, name='student_edit'),
    path('student/<int:nid>/delete/', student.student_delete, name='student_delete'),

    # 部门
    path('department/', department.department, name='department'),
    path('department/add/', department.department_add, name='department_add'),
    path('department/<int:nid>/edit/', department.department_edit, name='department_edit'),
    path('department/<int:nid>/delete/', department.department_delete, name='department_delete'),

    # 公司
    path('company/', company.company, name='company'),
    path('company/add/', company.company_add, name='company_add'),
    path('company/<int:nid>/edit/', company.company_edit, name='company_edit'),
    path('company/<int:nid>/delete/', company.company_delete, name='company_delete'),

    # 岗位
    path('position/', position.position, name='position'),
    path('position/add/', position.position_add, name='position_add'),
    path('position/<int:nid>/edit/', position.position_edit, name='position_edit'),
    path('position/<int:nid>/delete/', position.position_delete, name='position_delete'),

    # 航空器类型
    path('aircraft_type/', aircraft_type.aircraft_type, name='aircraft_type'),
    path('aircraft_type/add/', aircraft_type.aircraft_type_add, name='aircraft_type_add'),
    path('aircraft_type/<int:nid>/edit/', aircraft_type.aircraft_type_edit, name='aircraft_type_edit'),
    path('aircraft_type/<int:nid>/delete/', aircraft_type.aircraft_type_delete, name='aircraft_type_delete'),

    # 航空器
    path('aircraft/', aircraft.aircraft, name='aircraft'),
    path('aircraft/add/', aircraft.aircraft_add, name='aircraft_add'),
    path('aircraft/<int:nid>/edit/', aircraft.aircraft_edit, name='aircraft_edit'),
    path('aircraft/<int:nid>/delete/', aircraft.aircraft_delete, name='aircraft_delete'),

    # 飞行课程
    path('flight_course/', flight_course.flight_course, name='flight_course'),
    path('flight_course/add/', flight_course.flight_course_add, name='flight_course_add'),
    path('flight_course/<int:nid>/edit/', flight_course.flight_course_edit, name='flight_course_edit'),
    path('flight_course/<int:nid>/delete/', flight_course.flight_course_delete, name='flight_course_delete'),

    # 飞行时间记录
    path('flight_record/', flight_record.flight_record, name='flight_record'),
    path('flight_record/add/', flight_record.flight_record_add, name='flight_record_add'),
    path('flight_record/<int:nid>/edit/', flight_record.flight_record_edit, name='flight_record_edit'),
    path('flight_record/<int:nid>/delete/', flight_record.flight_record_delete, name='flight_record_delete'),
    path('get_aircraft_type/', flight_record.get_aircraft_type, name='get_aircraft_type'),
    path('get_course_info/', flight_record.get_course_info, name='get_course_info'),
    path('get_persons/', flight_record.get_persons, name='get_persons'),

    # 系统管理
    path('users/', admin.user_list, name='users'),
    path('users/add/', admin.user_edit, name='users_add'),
    path('users/<int:user_id>/edit', admin.user_edit, name='users_edit'),
    path('users/<int:user_id>/delete/', admin.user_delete, name='users_delete'),
    path('get_user_groups/<int:user_id>/', admin.get_user_groups, name='get_user_groups'),
    path('get_groups/', admin.get_groups, name='get_groups'),
    path('groups/', admin.group_list, name='groups'),
    path('groups/add/', admin.group_edit, name='groups_add'),
    path('groups/<int:group_id>/edit', admin.group_edit, name='groups_edit'),
    path('groups/<int:group_id>/delete/', admin.group_delete, name='groups_delete'),
    path('groups/<int:group_id>/permissions/', admin.group_permissions, name='groups_permissions'),

    path('auth_dashboard/', custom_auth.custom_auth_dashboard, name='auth_dashboard'),

]
