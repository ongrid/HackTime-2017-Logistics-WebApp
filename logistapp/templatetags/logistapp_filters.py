from django import template

from logistapp.models import *

register = template.Library()


@register.inclusion_tag('logistapp/tags/item.html')
def print_item(item):
    return {'item': item}


@register.filter('get_elevation_type')
def get_elevation_type(ele_type):
    if ele_type == 'in':
        return 'Arrived at'
    return 'Left'
