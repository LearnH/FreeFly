from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from django import forms

from fly import models as fly_models
from fly.utils import pagination, permission_dict
from fly.utils.bootstrap import BaseModelForm


class FlightCourseForm(BaseModelForm):
    class Meta:
        model = fly_models.FlightCourse
        exclude = ('is_deleted','created_at','updated_at', 'created_by', 'updated_by')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 设置状态字段为单选按钮
        radio_list = ['device_type', 'aircraft_nature', 'field_transition', 'fly_nature', 'day_night', 'fly_category', 'status']
        for item in radio_list:
            choices = getattr(fly_models.FlightCourse, f'{item}_choices', None)
            if choices is not None:
                self.fields[item].widget = forms.RadioSelect(choices=choices)
            elif item == 'device_type':
                self.fields[item].widget = forms.RadioSelect(choices=fly_models.Aircraft.device_type_choices)
            elif item == 'aircraft_nature':
                self.fields[item].widget = forms.RadioSelect(choices=fly_models.AircraftType.aircraft_nature_choices)
            else:
                raise AttributeError(f"{item}_choices does not exist in FlightCourse model.")
        self.fields['status'].initial = 1



@login_required
@permission_required('fly.view_flightcourse', raise_exception=True)
def flight_course(request):
    data_dict = {'is_deleted': False}
    key_query = request.GET.get('searchKey', '').strip()
    status_query = request.GET.get('searchStatus', '').strip()
    if key_query:
        data_dict['name__contains'] = key_query
    if status_query:
        data_dict['status'] = status_query

    # 构建查询集
    queryset = fly_models.FlightCourse.objects.filter(**data_dict)
    status_choices = fly_models.FlightCourse.status_choices
    # 应用分页
    page_obj = pagination.Pagination(request, queryset)
    permissions = permission_dict.get_model_permission(fly_models.FlightCourse)
    context = {
        'flight_course_list': page_obj.page_queryset,
        'page_string': page_obj.page_html(),
        'key_query': key_query,
        'status_query': status_query,
        'status_choices': status_choices,
    }
    context.update(permissions)
    return render(request, 'flight_course.html', context)


@login_required
@permission_required('fly.add_flightcourse', raise_exception=True)
def flight_course_add(request):
    if request.method == 'POST':
        form = FlightCourseForm(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            form.save()
            return redirect('flight_course')  # 重定向到项目列表页
    else:
        form = FlightCourseForm()

    context = {
        'form': form,
        'theme': '课程',
        'back_url': 'flight_course',
    }

    return render(request, 'base/base_form.html', context)


@login_required
@permission_required('fly.change_flightcourse', raise_exception=True)
def flight_course_edit(request, nid):
    row_object = fly_models.FlightCourse.objects.filter(id=nid).first()
    if request.method == 'POST':
        form = FlightCourseForm(request.POST, request.FILES, instance=row_object)
        if form.is_valid():
            form.save()
            return redirect('flight_course')
    else:
        form = FlightCourseForm(instance=row_object)

    context = {
        'form': form,
        'theme': '课程',
        'back_url': 'flight_course',
    }

    return render(request, 'base/base_form.html', context)


@login_required
@permission_required('fly.delete_flightcourse', raise_exception=True)
def flight_course_delete(request, nid):
    # 获取对应ID的对象，如果不存在则返回404
    obj = get_object_or_404(fly_models.FlightCourse, id=nid)
    obj.is_deleted = True
    obj.save()
    return redirect('flight_course')
