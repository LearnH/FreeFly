import json
import logging

from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.db.models import Q, Count
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

from django import forms
from django.utils import timezone

from fly.utils import pagination, permission_dict


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name',
                  'is_active', 'is_staff', 'is_superuser')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name',
                  'is_active', 'is_staff', 'is_superuser')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        user = super().save(commit=False)

        # 设置密码
        password = self.cleaned_data.get('password1')
        if password:
            user.set_password(password)

        # 设置加入日期（仅对新用户）
        if not user.pk:
            user.date_joined = timezone.now()

        if commit:
            user.save()
            self.save_m2m()  # 保存多对多关系

        return user

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = '__all__'  # 或指定具体字段，如 ['name']


@login_required
@permission_required('auth.view_user', raise_exception=True)
def user_list(request):
    key_query = request.GET.get('searchKey', '').strip()

    # 构造查询条件
    query = Q()
    if key_query:
        query |= Q(username__icontains=key_query)
        query |= Q(first_name__icontains=key_query)
        query |= Q(last_name__icontains=key_query)

    users = User.objects.filter(query)
    page_obj = pagination.Pagination(request, users)  # 应用分页
    permissions = permission_dict.get_model_permission(User)
    context = {
        'users': page_obj.page_queryset,
        'page_string': page_obj.page_html(),
        'key_query': key_query,
    }
    context.update(permissions)
    return render(request, 'admin/user_list.html', context)

@login_required
@permission_required('auth.change_uer', raise_exception=True)
def user_edit(request, user_id=None):
    user = None
    if user_id:
        user = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        try:
            print('POST 数据:', request.POST)
            # 处理用户组关系
            group_data = request.POST.get('selectedGroupsInput', '[]')
            print(group_data)
            try:
                group_ids = json.loads(group_data)
                group_ids = [int(id) for id in group_ids]
            except (json.decoder.JSONDecodeError, TypeError, ValueError):
                group_ids = []

            # 创建表单实例
            if user_id:
                form = CustomUserChangeForm(request.POST, instance=user)
            else:
                form = CustomUserCreationForm(request.POST)

            # 保存用户信息
            if form.is_valid():
                user = form.save()
                user.groups.set(group_ids)
                messages.success(request, '用户信息已成功保存')
                return redirect(reverse('users'))
            else:
                print("表单无效")  # 调试
                print(f"错误信息: {form.errors}")
                messages.error(request, '表单验证失败，请检查输入。')
        except Exception as e:
            print(f"保存用户信息时出错: {e}")
            messages.error(request, '保存用户信息时出错：{}'.format(e))
    else:
        if user_id:
            form = CustomUserChangeForm(instance=user)
        else:
            form = CustomUserCreationForm()
    # 传递已选择的用户组ID到模板
    selected_group_ids = user.groups.values_list('id', flat=True) if user else []
    context = {
        'form': form,
        'user_id': user_id,
        'theme': '用户',
        'back_url': 'users',
        'selected_group_ids': list(selected_group_ids),
    }

    return render(request, 'admin/user_form.html', context)

@login_required
@permission_required('auth.delete_user', raise_exception=True)
def user_delete(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.delete()
    messages.success(request, '用户已成功删除')
    return redirect(reverse('users'))

@login_required
def get_user_groups(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    groups = user.groups.all()
    return JsonResponse([{
        'id': group.id,
        'name': group.name
    } for group in groups], safe=False)

@login_required
def get_groups(request):
    groups = Group.objects.all()
    return JsonResponse([{
        'id': group.id,
        'name': group.name,
        'memberCount': group.user_set.count()
    } for group in groups], safe=False)

@login_required
@permission_required('auth.view_user', raise_exception=True)
def user_permissions(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        selected_permissions = request.POST.getlist('permissions')
        user.user_permissions.set(selected_permissions)
        messages.success(request, '用户权限已更新')
        return redirect(reverse('user_edit', args=[user_id]))
    else:
        all_permissions = Permission.objects.all()
        user_permissions = list(user.user_permissions.values_list('id', flat=True))
        return render(request, '#', {
            'user': user,
            'all_permissions': all_permissions,
            'user_permissions': user_permissions
        })

@login_required
@permission_required('auth.view_group', raise_exception=True)
def group_list(request):
    key_query = request.GET.get('searchKey', '').strip()
    # 构造查询条件
    query = Q()
    if key_query:
        query |= Q(name__icontains=key_query)
    groups = Group.objects.filter(query)
    page_obj = pagination.Pagination(request, groups)  # 应用分页
    permissions = permission_dict.get_model_permission(Group)
    context = {
        'groups': page_obj.page_queryset,
        'page_string': page_obj.page_html(),
        'key_query': key_query,
    }
    context.update(permissions)
    return render(request, 'admin/group_list.html', context)

@login_required
@permission_required('auth.add_group', raise_exception=True)
def group_edit(request, group_id=None):
    group_permissions = []
    if group_id:
        group = get_object_or_404(Group, pk=group_id)
        group_permissions = list(group.permissions.values_list('id', flat=True))
        form = GroupForm(request.POST or None, instance=group)
    else:
        form = GroupForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, '用户组信息已成功保存')
        return redirect(reverse('groups'))
    all_permissions = Permission.objects.all()
    context = {
        'form': form,
        'group_id': group_id,
        'all_permissions': all_permissions,
        'group_permissions': group_permissions,
        'theme': '用户组',
        'back_url': 'groups',
    }
    return render(request, 'admin/group_form.html', context)

@login_required
@permission_required('auth.delete_group', raise_exception=True)
def group_delete(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    group.delete()
    messages.success(request, '用户组已成功删除')
    return redirect(reverse('groups'))

@staff_member_required
@login_required
def group_permissions(request, group_id):
    group = get_object_or_404(Group, pk=group_id)

    if request.method == 'POST':
        selected_permissions = request.POST.getlist('permissions')
        group.permissions.set(selected_permissions)
        messages.success(request, '用户组权限已更新')
        return redirect(reverse('groups'))

    all_permissions = Permission.objects.all()
    group_permissions = list(group.permissions.values_list('id', flat=True))

    return render(request, 'admin/group_permissions.html', {
        'group': group,
        'all_permissions': all_permissions,
        'group_permissions': group_permissions,
    })
