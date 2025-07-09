from django import template

register = template.Library()

@register.filter
def sum_flight_sortie(queryset):
    """计算起落架次总和"""
    return sum(record.flight_sortie for record in queryset if record.flight_sortie)