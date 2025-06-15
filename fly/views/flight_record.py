from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from django import forms

from fly import models as fly_models
from fly.utils import pagination
from fly.utils.bootstrap import BaseModelForm


class FlightRecordForm(BaseModelForm):
    class Meta:
        model = fly_models.FlightRecord
        exclude = ('is_deleted', 'created_at', 'updated_at')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 设置状态字段为单选按钮
        radio_list = ['field_transition', 'fly_nature', 'day_night', 'fly_category']
        for item in radio_list:
            choices = getattr(fly_models.FlightRecord, f'{item}_choices', None)
            if choices is not None:
                self.fields[item].widget = forms.RadioSelect(choices=choices)
            elif item == 'fly_category':
                self.fields[item].widget = forms.RadioSelect(choices=fly_models.FlightCourse.fly_category_choices)
            else:
                raise AttributeError(f"{item}_choices does not exist in FlightRecord model.")


@login_required
@permission_required('fly.view_flight_record', raise_exception=True)
def flight_record(request):
    data_dict = {'is_deleted': False}
    key_query = request.GET.get('searchKey', '').strip()
    status_query = request.GET.get('searchStatus', '').strip()
    task_pilot_query = request.GET.get('searchTaskPilot', '').strip()
    start_date_query = request.GET.get('startDate', '').strip()
    end_date_query = request.GET.get('endDate', '').strip()
    if key_query:
        data_dict['remark__contains'] = key_query
    if status_query:
        data_dict['fly_category'] = status_query
    if task_pilot_query:
        data_dict['task_pilot'] = task_pilot_query

    # 处理日期区间查询
    if start_date_query and end_date_query:
        data_dict['flight_date__range'] = [start_date_query, end_date_query]
    elif start_date_query:
        data_dict['flight_date__gte'] = start_date_query
    elif end_date_query:
        data_dict['flight_date__lte'] = end_date_query

    # 构建查询集
    queryset = fly_models.FlightRecord.objects.filter(**data_dict)
    fly_category_choices = fly_models.FlightCourse.fly_category_choices
    task_pilot_list = fly_models.Employee.objects.filter(is_deleted=False)
    # 应用分页
    page_obj = pagination.Pagination(request, queryset)
    context = {
        'flight_record_list': page_obj.page_queryset,
        'page_string': page_obj.page_html(),
        'key_query': key_query,
        'status_query': status_query,
        'status_choices': fly_category_choices,
        'task_pilot_query': task_pilot_query,
        'task_pilot_list': task_pilot_list,
        'start_date_query': start_date_query,
        'end_date_query': end_date_query,
    }

    return render(request, 'flight_record.html', context)


@login_required
@permission_required('fly.add_flight_record', raise_exception=True)
def flight_record_add(request):
    if request.method == 'POST':
        form = FlightRecordForm(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            form.save()
            return redirect('flight_record')  # 重定向到项目列表页
    else:
        form = FlightRecordForm()

    date_fields = ['flight_date']
    time_fields = ['open_time', 'takeoff_time', 'landing_time', 'close_time']

    context = {
        'form': form,
        'theme': '课程',
        'back_url': 'flight_record',
        'date_fields': date_fields,
        'time_fields': time_fields,
    }

    return render(request, 'base/base_form.html', context)


@login_required
@permission_required('fly.change_flight_record', raise_exception=True)
def flight_record_edit(request, nid):
    row_object = fly_models.FlightRecord.objects.filter(id=nid).first()
    if request.method == 'POST':
        form = FlightRecordForm(request.POST, request.FILES, instance=row_object)
        if form.is_valid():
            form.save()
            return redirect('flight_record')
    else:
        form = FlightRecordForm(instance=row_object)

    date_fields = ['flight_date']
    time_fields = ['open_time', 'takeoff_time', 'landing_time', 'close_time']

    context = {
        'form': form,
        'theme': '课程',
        'back_url': 'flight_record',
        'date_fields': date_fields,
        'time_fields': time_fields,
    }

    return render(request, 'base/base_form.html', context)


@login_required
@permission_required('fly.delete_flight_record', raise_exception=True)
def flight_record_delete(request, nid):
    # 获取对应ID的对象，如果不存在则返回404
    obj = get_object_or_404(fly_models.FlightRecord, id=nid)
    obj.is_deleted = True
    obj.save()
    return redirect('flight_record')
