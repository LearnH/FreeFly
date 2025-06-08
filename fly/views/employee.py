from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from django import forms

from fly import models as fly_models
from fly.utils import pagination
from fly.utils.bootstrap import BaseModelForm


class EmployeeForm(BaseModelForm):
    class Meta:
        model = fly_models.Employee
        # fields = '__all__'
        fields = ['emp_code', 'name', 'photo', 'gender', 'nationality', 'ID_type', 'ID_number', 'birth_date',
                  'nation', 'native_place', 'address', 'phone', 'email', 'political_status', 'marital_status',
                  'education_level', 'emergency_contact_name', 'emergency_contact_phone',
                  'emergency_contact_relationship',
                  'ope_base', 'employment_type', 'employment_date', 'confirmable_date', 'company', 'department',
                  'position', 'is_coach',
                  'status', 'termination_date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 设置状态字段为单选按钮
        radio_list = [
            'gender', 'marital_status', 'emergency_contact_relationship', 'employment_type', 'status', 'education_level'
        ]
        for item in radio_list:
            # 动态获取属性，例如 item="gender" → Employee.gender_choices
            choices = getattr(fly_models.Employee, f"{item}_choices", None)
            if choices is not None:
                self.fields[item].widget = forms.RadioSelect(choices=choices)
            else:
                raise AttributeError(f"{item}_choices does not exist in Employee model.")

        # 定义需要过滤的字段和对应模型
        filter_fields = {
            'company': fly_models.Company,
            'department': fly_models.Department,
            'position': fly_models.Position,
        }

        # 循环设置 queryset
        for field_name, model in filter_fields.items():
            if field_name in self.fields:
                self.fields[field_name].queryset = model.objects.filter(is_deleted=False)

        self.fields['status'].initial = 1
        self.fields['gender'].initial = 1


@login_required
@permission_required('fly.view_employee', raise_exception=True)
def employee(request):
    data_dict = {'is_deleted': False}
    key_query = request.GET.get('searchKey', '').strip()
    status_query = request.GET.get('searchStatus', '').strip()
    emp_code_query = request.GET.get('searchCode', '').strip()
    if key_query:
        data_dict['name__contains'] = key_query
    if status_query:
        data_dict['status'] = status_query
    if emp_code_query:
        data_dict['emp_code__contains'] = emp_code_query

    # 构建查询集
    queryset = fly_models.Employee.objects.filter(**data_dict)
    status_choices = fly_models.Employee.status_choices
    # 应用分页
    page_obj = pagination.Pagination(request, queryset)
    context = {
        'employee_list': page_obj.page_queryset,
        'page_string': page_obj.page_html(),
        'status_choices': status_choices,
        'key_query': key_query,
        'status_query': status_query,
        'emp_code_query': emp_code_query,
    }

    return render(request, 'employee.html', context)


@login_required
@permission_required('fly.add_employee', raise_exception=True)
def employee_add(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        print(form.errors)
        if form.is_valid():
            form.save()
            return redirect('employee')  # 重定向到项目列表页
    else:
        form = EmployeeForm()

    date_fields = ['birth_date', 'employment_date', 'confirmable_date', 'termination_date']
    context = {
        'form': form,
        'theme': '员工',
        'back_url': 'employee',
        'date_fields': date_fields,
    }

    return render(request, 'base/base_form.html', context)


@login_required
@permission_required('fly.change_employee', raise_exception=True)
def employee_edit(request, nid):
    row_object = fly_models.Employee.objects.filter(id=nid).first()
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=row_object)
        if form.is_valid():
            form.save()
            return redirect('employee')
    else:
        form = EmployeeForm(instance=row_object)
    date_fields = ['birth_date', 'employment_date', 'confirmable_date', 'termination_date']
    context = {
        'form': form,
        'theme': '员工',
        'back_url': 'employee',
        'date_fields': date_fields,
    }

    return render(request, 'base/base_form.html', context)


@login_required
@permission_required('fly.delete_employee', raise_exception=True)
def employee_delete(request, nid):
    # 获取对应ID的对象，如果不存在则返回404
    obj = get_object_or_404(fly_models.Employee, id=nid)
    obj.is_deleted = True
    obj.save()
    return redirect('employee')
