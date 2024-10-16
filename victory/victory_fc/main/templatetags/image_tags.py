# yourapp/templatetags/image_tags.py
from django import template

register = template.Library()

@register.simple_tag
def lazy_image(src, alt="Image", **kwargs):
    kwargs_str = " ".join([f'{key}="{value}"' for key, value in kwargs.items()])
    return f'<img src="{src}" alt="{alt}" loading="lazy" {kwargs_str}>'
