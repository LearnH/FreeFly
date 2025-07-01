from django import template

register = template.Library()
@register.filter
def has_permission(user, permission_name):
    if not permission_name: # 处理空权限字符串
        return False
    return user.has_perm(permission_name)