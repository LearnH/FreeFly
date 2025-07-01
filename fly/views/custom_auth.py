from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import Count
from datetime import datetime, timedelta
from fly.models import ProxyUser, ProxyGroup, ProxyPermission


@staff_member_required
def custom_auth_dashboard(request):
    # 用户统计
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    inactive_users = total_users - active_users
    staff_users = User.objects.filter(is_staff=True).count()
    superusers = User.objects.filter(is_superuser=True).count()

    # 组统计
    group_count = ProxyGroup.objects.count()
    permission_count = ProxyPermission.objects.count()

    # 用户创建趋势（最近30天）
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)

    creation_counts = []
    creation_dates = []

    current_date = start_date
    while current_date <= end_date:
        count = User.objects.filter(
            date_joined__date=current_date.date()
        ).count()
        creation_counts.append(count)
        creation_dates.append(current_date.strftime("%m-%d"))
        current_date += timedelta(days=1)

    context = {
        'user_count': total_users,
        'active_count': active_users,
        'inactive_count': inactive_users,
        'staff_count': staff_users,
        'superuser_count': superusers,
        'group_count': group_count,
        'permission_count': permission_count,

        'user_list_url': reverse('admin:fly_proxyuser_changelist'),
        'group_list_url': reverse('admin:fly_proxygroup_changelist'),
        'add_user_url': reverse('admin:fly_proxyuser_add'),
        'add_group_url': reverse('admin:fly_proxygroup_add'),
        'permission_list_url': reverse('admin:fly_proxypermission_changelist'),

        'creation_counts': creation_counts,
        'creation_dates': creation_dates,
    }
    return render(request, 'admin/dashboard.html', context)