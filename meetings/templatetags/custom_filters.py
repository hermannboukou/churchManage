from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, 0)

# hearing/templatetags/custom_filters.py
@register.filter(name='split')
def split(value, key):
    return value.split(key)

# Dans templatetags/custom_filters.py
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, '')

@register.filter
def get_item(dictionary, key):
    return dictionary.get(str(key), '')  # Conversion en string pour sécurité


@register.filter
def sum_attr(queryset, attr):
    return sum(getattr(item, attr, 0) for item in queryset)



