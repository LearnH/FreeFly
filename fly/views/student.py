from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from django import forms

from fly import models as fly_models
from fly.utils import pagination, permission_dict
from fly.utils.bootstrap import BaseModelForm


class StudentForm(BaseModelForm):
    class Meta:
        model = fly_models.Student
        # fields = '__all__'
        fields = ['stu_code', 'name', 'photo', 'gender', 'nationality', 'ID_type', 'ID_number', 'birth_date',
                  'nation', 'native_place', 'address', 'phone', 'email', 'political_status',
                  'education_level', 'emergency_contact_name', 'emergency_contact_phone',
                  'emergency_contact_relationship',
                  'ope_base', 'company', 'student_type', 'enter_date', 'registration_date', 'is_temporary',
                  'status', 'termination_date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 设置状态字段为单选按钮
        radio_list = [
            'gender', 'emergency_contact_relationship', 'student_type', 'status', 'education_level'
        ]
        for item in radio_list:
            # 动态获取属性，例如 item="gender" → Student.gender_choices
            choices = getattr(fly_models.Student, f"{item}_choices", None)
            if choices is not None:
                self.fields[item].widget = forms.RadioSelect(choices=choices)
            else:
                raise AttributeError(f"{item}_choices does not exist in Student model.")

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
@permission_required('fly.view_student', raise_exception=True)
def student(request):
    data_dict = {'is_deleted': False}
    key_query = request.GET.get('searchKey', '').strip()
    status_query = request.GET.get('searchStatus', '').strip()
    stu_code_query = request.GET.get('searchCode', '').strip()
    if key_query:
        data_dict['name__contains'] = key_query
    if status_query:
        data_dict['status'] = status_query
    if stu_code_query:
        data_dict['stu_code__contains'] = stu_code_query

    # 构建查询集
    queryset = fly_models.Student.objects.filter(**data_dict)
    status_choices = fly_models.Student.status_choices
    # 应用分页
    page_obj = pagination.Pagination(request, queryset)
    permissions = permission_dict.get_model_permission(fly_models.Student)
    context = {
        'student_list': page_obj.page_queryset,
        'page_string': page_obj.page_html(),
        'status_choices': status_choices,
        'key_query': key_query,
        'status_query': status_query,
        'stu_code_query': stu_code_query,
    }
    context.update(permissions)
    return render(request, 'student.html', context)


@login_required
@permission_required('fly.add_student', raise_exception=True)
def student_add(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.created_by = request.user
            obj.updated_by = request.user
            obj.save()
            return redirect('student')  # 重定向到项目列表页
    else:
        form = StudentForm()

    date_fields = ['birth_date', 'enter_date', 'registration_date', 'termination_date']
    image_fields = ['photo']
    context = {
        'form': form,
        'theme': '学员',
        'back_url': 'student',
        'date_fields': date_fields,
        'image_fields': image_fields,
    }

    return render(request, 'base/base_form.html', context)


@login_required
@permission_required('fly.change_student', raise_exception=True)
def student_edit(request, nid):
    row_object = fly_models.Student.objects.filter(id=nid).first()
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=row_object)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.updated_by = request.user
            obj.save()
            return redirect('student')
    else:
        form = StudentForm(instance=row_object)
    date_fields = ['birth_date', 'enter_date', 'registration_date', 'termination_date']
    image_fields = ['photo']
    context = {
        'form': form,
        'theme': '学员',
        'back_url': 'student',
        'date_fields': date_fields,
        'image_fields': image_fields,
    }

    return render(request, 'base/base_form.html', context)


@login_required
@permission_required('fly.delete_student', raise_exception=True)
def student_delete(request, nid):
    # 获取对应ID的对象，如果不存在则返回404
    obj = get_object_or_404(fly_models.Student, id=nid)
    obj.is_deleted = True
    obj.save()
    return redirect('student')
