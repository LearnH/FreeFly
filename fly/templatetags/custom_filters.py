from django import template

register = template.Library()

@register.filter
def startswith(value, arg):
    """自定义 startswith 过滤器"""
    if value is None or arg is None:
        return False
    return str(value).startswith(str(arg))