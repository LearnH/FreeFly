from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from django import forms

from fly import models as fly_models
from fly.utils import pagination
from fly.utils.bootstrap import BaseModelForm


class AircraftTypeForm(BaseModelForm):
    class Meta:
        model = fly_models.AircraftType
        exclude = ('is_deleted','created_at','updated_at')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 设置状态字段为单选按钮
        radio_list = ['aircraft_nature', 'status']
        for item in radio_list:
            choices = getattr(fly_models.AircraftType, f'{item}_choices', None)
            if choices is not None:
                self.fields[item].widget = forms.RadioSelect(choices=choices)
            else:
                raise AttributeError(f"{item}_choices does not exist in AircraftType model.")
        self.fields['status'].initial = 1



@login_required
@permission_required('fly.view_aircraft_type', raise_exception=True)
def aircraft_type(request):
    data_dict = {'is_deleted': False}
    key_query = request.GET.get('searchKey', '').strip()
    status_query = request.GET.get('searchStatus', '').strip()
    if key_query:
        data_dict['name__contains'] = key_query
    if status_query:
        data_dict['status'] = status_query

    # 构建查询集
    queryset = fly_models.AircraftType.objects.filter(**data_dict)
    status_choices = fly_models.AircraftType.status_choices
    # 应用分页
    page_obj = pagination.Pagination(request, queryset)
    context = {
        'aircraft_type_list': page_obj.page_queryset,
        'page_string': page_obj.page_html(),
        'status_choices': status_choices,
        'key_query': key_query,
        'status_query': status_query,
    }

    return render(request, 'basic_archives/aircraft_type.html', context)


@login_required
@permission_required('fly.add_aircraft_type', raise_exception=True)
def aircraft_type_add(request):
    if request.method == 'POST':
        form = AircraftTypeForm(request.POST)
        print(form.errors)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.created_by = request.user
            obj.updated_by = request.user
            obj.save()
            return redirect('aircraft_type')  # 重定向到项目列表页
    else:
        form = AircraftTypeForm()

    context = {
        'form': form,
        'theme': '机型',
        'back_url': 'aircraft_type',
    }

    return render(request, 'base/base_form.html', context)


@login_required
@permission_required('fly.change_aircraft_type', raise_exception=True)
def aircraft_type_edit(request, nid):
    row_object = fly_models.AircraftType.objects.filter(id=nid).first()
    if request.method == 'POST':
        form = AircraftTypeForm(request.POST, instance=row_object)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.updated_by = request.user
            obj.save()
            return redirect('aircraft_type')
    else:
        form = AircraftTypeForm(instance=row_object)

    context = {
        'form': form,
        'theme': '机型',
        'back_url': 'aircraft_type',
    }

    return render(request, 'base/base_form.html', context)


@login_required
@permission_required('fly.delete_aircraft_type', raise_exception=True)
def aircraft_type_delete(request, nid):
    # 获取对应ID的对象，如果不存在则返回404
    obj = get_object_or_404(fly_models.AircraftType, id=nid)
    obj.is_deleted = True
    obj.save()
    return redirect('aircraft_type')
