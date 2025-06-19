import datetime
from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django import forms

from fly import models as fly_models
from fly.utils import pagination
from fly.utils.bootstrap import BaseModelForm

class FlightRecordForm(BaseModelForm):
    flight_duration_display = forms.CharField(label="飞行时长", required=False)
    class Meta:
        model = fly_models.FlightRecord
        fields = ['flight_date', 'task_pilot', 'flight_course', 'field_transition','fly_nature',
                  'day_night', 'fly_category', 'aircraft', 'aircraft_type', 'departure_airport',
                  'arrival_airport', 'open_time', 'take_off_time', 'landing_time', 'close_time',
                  'flight_duration', 'flight_duration_display', 'flight_sortie', 'left_seat_person',
                  'right_seat_person', 'remark']

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

        # 隐藏实际存储的分钟字段flight_duration
        self.fields['flight_duration'].widget = forms.HiddenInput()
        if self.instance and self.instance.flight_duration:
            hours, remainder = divmod(self.instance.flight_duration, 60)
            self.fields['flight_duration_display'].initial = f"{hours:02d}:{remainder:02d}"

    def clean(self):
        cleaned_data = super().clean()
        open_time = cleaned_data.get('open_time')
        take_off_time = cleaned_data.get('take_off_time')
        landing_time = cleaned_data.get('landing_time')
        close_time = cleaned_data.get('close_time')
        flight_date = cleaned_data.get('flight_date')

        if open_time and take_off_time and landing_time and close_time:
            if open_time >= take_off_time or take_off_time >= landing_time or landing_time >= close_time:
                raise forms.ValidationError("时间顺序不正确，请重新输入。")

        if open_time and close_time:
            try:
                open_dt = datetime.datetime.combine(flight_date, open_time)
                close_dt = datetime.datetime.combine(flight_date, close_time)
                if open_dt >= close_dt:
                    raise forms.ValidationError("开车时间不能晚于关车时间。")
                cleaned_data['flight_duration'] = (close_dt - open_dt).seconds // 60
                hours, remainder = divmod(cleaned_data['flight_duration'], 60)
                cleaned_data['flight_duration_display'] = f"{hours:02d}:{remainder:02d}"
            except Exception as e:
                raise forms.ValidationError(f"计算飞行时间出错：{e}")
        else:
            # 如果没有提供时间，则清空 flight_duration
            cleaned_data['flight_duration'] = None
            cleaned_data['flight_duration_display'] = ''
        return cleaned_data

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
    time_fields = ['open_time', 'take_off_time', 'landing_time', 'close_time']

    context = {
        'form': form,
        'theme': '课程',
        'back_url': 'flight_record',
        'date_fields': date_fields,
        'time_fields': time_fields,
    }

    return render(request, 'flight_record_form.html', context)


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
    time_fields = ['open_time', 'take_off_time', 'landing_time', 'close_time']

    context = {
        'form': form,
        'theme': '课程',
        'back_url': 'flight_record',
        'date_fields': date_fields,
        'time_fields': time_fields,
    }

    return render(request, 'flight_record_form.html', context)


@login_required
@permission_required('fly.delete_flight_record', raise_exception=True)
def flight_record_delete(request, nid):
    # 获取对应ID的对象，如果不存在则返回404
    obj = get_object_or_404(fly_models.FlightRecord, id=nid)
    obj.is_deleted = True
    obj.save()
    return redirect('flight_record')

@login_required
def get_aircraft_type(request):
    aircraft_id = request.GET.get('aircraft_id', '')
    try:
        aircraft = fly_models.Aircraft.objects.get(id=aircraft_id)
        return JsonResponse({
            'success': True,
            'aircraft_type': aircraft.aircraft_type.name,
        })
    except fly_models.Aircraft.DoesNotExist:
        return JsonResponse({
           'success': False,
            'error': '航空器不存在',
        })

@login_required
def get_course_info(request):
    course_id = request.GET.get('flight_course_id', '')
    # 参数校验
    if not course_id.isdigit():
        return JsonResponse({
            'success': False,
            'error': '无效的课程ID',
        })

    try:
        course = fly_models.FlightCourse.objects.get(id=course_id)
        return JsonResponse({
            'success': True,
            'course_info': {
                'field_transition': course.field_transition,
                'fly_category': course.fly_category,
                'fly_nature': course.fly_nature,
                'day_night': course.day_night,
            },
        })
    except fly_models.FlightCourse.DoesNotExist:
        return JsonResponse({
           'success': False,
            'error': '课程不存在',
        })
