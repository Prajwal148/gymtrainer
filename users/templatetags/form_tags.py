# users/templatetags/form_tags.py
from django import template
from django.forms.widgets import RadioSelect


register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    return field.as_widget(attrs={'class': css_class})
@register.filter
def is_radio(field):
    return isinstance(field.field.widget, RadioSelect)