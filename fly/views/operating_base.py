from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404

from fly import models as fly_models
from fly.utils import pagination
from django import forms
from fly.utils.bootstrap import BaseModelForm

class OperatingBaseForm(BaseModelForm):
    class Meta:
        model = fly_models.OperatingBase
        fields = ['name', 'base_type', 'airport', 'address', 'in_charge', 'phone', 'description', 'status']

    def __init__(self, *args, **kwargs):
        airport_queryset = kwargs.pop('airport_queryset', None)  # 从kwargs中获取airport_queryset
        super().__init__(*args, **kwargs)

        if airport_queryset is not None:
            self.fields['airport'].queryset = airport_queryset
        else:
            # 默认只显示未删除的机场
            self.fields['airport'].queryset = fly_models.Airport.objects.filter(is_deleted=False)

        self.fields['base_type'].widget = forms.RadioSelect(
            choices=fly_models.OperatingBase.base_type_choices
        )
        # 设置状态字段为单选按钮
        self.fields['status'].widget = forms.RadioSelect(
            choices=fly_models.OperatingBase.status_choices
        )
        self.fields['status'].initial = 1

@login_required
@permission_required('fly.view_operating_base', raise_exception=True)
def operating_base(request):
    # 获取查询参数
    data_dict = {'is_deleted': False}
    key_query = request.GET.get('searchKey', '').strip()
    status_query = request.GET.get('searchStatus', '').strip()
    if key_query:
        data_dict['name__contains'] = key_query
    if status_query:
        data_dict['status'] = status_query

    # 构建查询集
    queryset = fly_models.OperatingBase.objects.filter(**data_dict)

    status_choices = fly_models.OperatingBase.status_choices

    # 应用分页
    page_obj = pagination.Pagination(request, queryset)

    context = {
        'ope_base_list': page_obj.page_queryset,
        'page_string': page_obj.page_html(),
        'status_choices': status_choices,
        'key_query': key_query,
        'status_query': status_query,
    }

    return render(request, 'operating_base.html', context)

@login_required
@permission_required('fly.add_operating_base', raise_exception=True)
def operating_base_add(request):
    if request.method == 'POST':
        form = OperatingBaseForm(request.POST)
        print(form.errors)
        if form.is_valid():
            form.save()
            return redirect('operating_base')  # 重定向到项目列表页
    else:
        airport_queryset = fly_models.Airport.objects.filter(is_deleted=False)  # 只显示未删除的机场
        form = OperatingBaseForm(initial={'status': 1}, airport_queryset=airport_queryset)

    return render(request, 'operating_base_form.html', {'form': form})

@login_required
@permission_required('fly.change_operating_base', raise_exception=True)
def operating_base_edit(request, nid):
    row_object = fly_models.OperatingBase.objects.filter(id=nid).first()
    if request.method == 'POST':
        form = OperatingBaseForm(request.POST, instance=row_object)
        if form.is_valid():
            form.save()
            return redirect('operating_base')
    else:
        form = OperatingBaseForm(instance=row_object)
    return render(request, 'operating_base_form.html', {'form': form})

@login_required
@permission_required('fly.delete_operating_base', raise_exception=True)
def operating_base_delete(request, nid):
    # 获取对应ID的基地对象，如果不存在则返回404
    obj = get_object_or_404(fly_models.OperatingBase, id=nid)
    obj.is_deleted = True
    obj.save()
    return redirect('operating_base')