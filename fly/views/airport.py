from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404

from fly import models as fly_models
from fly.utils import pagination
from django import forms
from fly.utils.bootstrap import BaseModelForm


class AirportForm(BaseModelForm):
    class Meta:
        model = fly_models.Airport
        # fields = '__all__'
        exclude = ('is_deleted', 'created_at', 'updated_at')
        # 定义字段顺序
        fields = ['name', 'icao_code', 'latitude', 'longitude', 'address', 'is_owner', 'is_air_harbor', 'is_temporary',
                  'is_tower', 'description', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 设置状态字段为单选按钮
        self.fields['status'].widget = forms.RadioSelect(
            choices=fly_models.Airport.status_choices
        )
        self.fields['status'].initial = 1


@login_required
@permission_required('fly.view_airport', raise_exception=True)
def airport(request):
    data_dict = {'is_deleted': False}
    key_query = request.GET.get('searchKey', '').strip()
    status_query = request.GET.get('searchStatus', '').strip()
    icao_query = request.GET.get('searchIcao', '').strip()
    if key_query:
        data_dict['name__contains'] = key_query
    if status_query:
        data_dict['status'] = status_query
    if icao_query:
        data_dict['icao_code__contains'] = icao_query

    # 构建查询集
    queryset = fly_models.Airport.objects.filter(**data_dict)
    status_choices = fly_models.Airport.status_choices
    # 应用分页
    page_obj = pagination.Pagination(request, queryset)
    context = {
        'airport_list': page_obj.page_queryset,
        'page_string': page_obj.page_html(),
        'status_choices': status_choices,
        'key_query': key_query,
        'status_query': status_query,
        'icao_query': icao_query,
    }

    return render(request, 'airport.html', context)


@login_required
@permission_required('fly.add_airport', raise_exception=True)
def airport_add(request):
    if request.method == 'POST':
        form = AirportForm(request.POST)
        print(form.errors)
        if form.is_valid():
            form.save()
            return redirect('airport')  # 重定向到项目列表页
    else:
        form = AirportForm(initial={'status': 1})

    return render(request, 'airport_form.html', {'form': form})


@login_required
@permission_required('fly.change_airport', raise_exception=True)
def airport_edit(request, nid):
    row_object = fly_models.Airport.objects.filter(id=nid).first()
    if request.method == 'POST':
        form = AirportForm(request.POST, instance=row_object)
        if form.is_valid():
            form.save()
            return redirect('airport')
    else:
        form = AirportForm(instance=row_object)

    return render(request, 'airport_form.html', {'form': form})


@login_required
@permission_required('fly.delete_airport', raise_exception=True)
def airport_delete(request, nid):
    # 获取对应ID的机场对象，如果不存在则返回404
    obj = get_object_or_404(fly_models.Airport, id=nid)
    obj.is_deleted = True
    obj.save()
    return redirect('airport')
