from django.contrib.auth.decorators import login_required, permission_required
from django.forms.widgets import TextInput
from django.shortcuts import render, redirect, get_object_or_404
from django import forms

from fly import models as fly_models
from fly.utils import pagination
from fly.utils.bootstrap import BaseModelForm


class CompanyForm(BaseModelForm):
    class Meta:
        model = fly_models.Company
        # fields = '__all__'
        # 定义字段顺序
        fields = ['name', 'name_en', 'name_short', 'parent', 'found_time', 'legal_person', 'phone',
                  'email', 'website', 'address', 'business_scope', 'description', 'address', 'business_scope','status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 设置状态字段为单选按钮
        self.fields['status'].widget = forms.RadioSelect(
            choices=fly_models.Company.status_choices
        )
        self.fields['status'].initial = 1



@login_required
@permission_required('fly.view_company', raise_exception=True)
def company(request):
    data_dict = {'is_deleted': False}
    key_query = request.GET.get('searchKey', '').strip()
    status_query = request.GET.get('searchStatus', '').strip()
    name_en_query = request.GET.get('searchNameEn', '').strip()
    if key_query:
        data_dict['name__contains'] = key_query
    if status_query:
        data_dict['status'] = status_query
    if name_en_query:
        data_dict['name_en__contains'] = name_en_query

    # 构建查询集
    queryset = fly_models.Company.objects.filter(**data_dict)
    status_choices = fly_models.Company.status_choices
    # 应用分页
    page_obj = pagination.Pagination(request, queryset)
    context = {
        'company_list': page_obj.page_queryset,
        'page_string': page_obj.page_html(),
        'status_choices': status_choices,
        'key_query': key_query,
        'status_query': status_query,
        'name_en_query': name_en_query,
    }

    return render(request, 'organization/company.html', context)


@login_required
@permission_required('fly.add_company', raise_exception=True)
def company_add(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        print(form.errors)
        if form.is_valid():
            form.save()
            return redirect('company')  # 重定向到项目列表页
    else:
        form = CompanyForm(initial={'status': 1})

    date_fields = ['found_time']

    context = {
        'form': form,
        'theme': '公司',
        'back_url': 'company',
        'date_fields': date_fields,
    }

    return render(request, 'base/base_form.html', context)


@login_required
@permission_required('fly.change_company', raise_exception=True)
def company_edit(request, nid):
    row_object = fly_models.Company.objects.filter(id=nid).first()
    if request.method == 'POST':
        form = CompanyForm(request.POST, instance=row_object)
        if form.is_valid():
            form.save()
            return redirect('company')
    else:
        form = CompanyForm(instance=row_object)

    date_field = ['found_time']

    context = {
        'form': form,
        'theme': '公司',
        'back_url': 'company',
        'date_field': date_field,
    }

    return render(request, 'base/base_form.html', context)


@login_required
@permission_required('fly.delete_company', raise_exception=True)
def company_delete(request, nid):
    # 获取对应ID的对象，如果不存在则返回404
    obj = get_object_or_404(fly_models.Company, id=nid)
    obj.is_deleted = True
    obj.save()
    return redirect('company')
