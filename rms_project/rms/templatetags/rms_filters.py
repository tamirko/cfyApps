from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def lower3(value):
    return value.lower()


@register.filter(name='cut2')
def cut2(value, arg):
    return value.replace(arg, '')


@register.filter(name='modulo')
def custom_modulo(num, val):
    return num % val


@register.filter
def running_cost(your_dict_list):
    return sum(d.current_cost for d in your_dict_list)


@register.filter
def replace_spaces_with_us(value):
    return value.replace(' ', '_')

@register.filter
def remove_spaces(value):
    return value.replace(' ', '')
