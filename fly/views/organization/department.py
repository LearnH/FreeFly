from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404

from fly import models as fly_models
from fly.utils import pagination
from django import forms
from fly.utils.bootstrap import BaseModelForm


class DepartmentForm(BaseModelForm):
    class Meta:
        model = fly_models.Department
        # fields = '__all__'
        # 定义字段顺序
        fields = ['name', 'parent', 'company', 'parent', 'description', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 设置状态字段为单选按钮
        self.fields['status'].widget = forms.RadioSelect(
            choices=fly_models.Department.status_choices
        )
        self.fields['status'].initial = 1

        # 定义需要过滤的字段和对应模型
        filter_fields = {
            'company': fly_models.Company,
        }

        # 循环设置 queryset
        for field_name, model in filter_fields.items():
            if field_name in self.fields:
                self.fields[field_name].queryset = model.objects.filter(is_deleted=False)


@login_required
@permission_required('fly.view_department', raise_exception=True)
def department(request):
    data_dict = {'is_deleted': False}
    key_query = request.GET.get('searchKey', '').strip()
    status_query = request.GET.get('searchStatus', '').strip()
    company_query = request.GET.get('searchCompany', '').strip()
    if key_query:
        data_dict['name__contains'] = key_query
    if status_query:
        data_dict['status'] = status_query
    if company_query:
        data_dict['company'] = company_query

    # 构建查询集
    queryset = fly_models.Department.objects.filter(**data_dict)
    status_choices = fly_models.Department.status_choices
    company_list = fly_models.Company.objects.filter(is_deleted=False)
    # 应用分页
    page_obj = pagination.Pagination(request, queryset)
    context = {
        'department_list': page_obj.page_queryset,
        'page_string': page_obj.page_html(),
        'status_choices': status_choices,
        'key_query': key_query,
        'status_query': status_query,
        'company_query': company_query,
        'company_list': company_list,
    }

    return render(request, 'organization/department.html', context)


@login_required
@permission_required('fly.add_department', raise_exception=True)
def department_add(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        print(form.errors)
        if form.is_valid():
            form.save()
            return redirect('department')  # 重定向到项目列表页
    else:
        form = DepartmentForm(initial={'status': 1})

    context = {
        'form': form,
        'theme': '部门',
        'back_url': 'department'
    }

    return render(request, 'base/base_form.html', context)


@login_required
@permission_required('fly.change_department', raise_exception=True)
def department_edit(request, nid):
    row_object = fly_models.Department.objects.filter(id=nid).first()
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=row_object)
        if form.is_valid():
            form.save()
            return redirect('department')
    else:
        form = DepartmentForm(instance=row_object)

    context = {
        'form': form,
        'theme': '部门',
        'back_url': 'department'
    }

    return render(request, 'base/base_form.html', context)


@login_required
@permission_required('fly.delete_department', raise_exception=True)
def department_delete(request, nid):
    # 获取对应ID的对象，如果不存在则返回404
    obj = get_object_or_404(fly_models.Department, id=nid)
    obj.is_deleted = True
    obj.save()
    return redirect('department')
