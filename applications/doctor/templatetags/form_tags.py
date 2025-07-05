from django import template
from django.utils.html import format_html
from django.forms.boundfield import BoundField
from django.utils.safestring import mark_safe
import re

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css):
    try:
        # Si es BoundField (un campo del formulario)
        if isinstance(field, BoundField):
            existing_classes = field.field.widget.attrs.get('class', '')
            # Evitar duplicar clases
            classes = existing_classes + ' ' + css if existing_classes else css
            # Copiar el widget y añadir clases
            widget = field.field.widget
            attrs = widget.attrs.copy()
            attrs['class'] = classes.strip()
            return field.as_widget(attrs=attrs)
        else:
            return field
    except Exception:
        return field
