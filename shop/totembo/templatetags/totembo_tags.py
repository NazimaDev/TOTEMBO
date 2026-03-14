from django import template
from django.urls import reverse
from totembo.models import Category

register = template.Library()


@register.simple_tag()
def main_categories():
    cats = Category.objects.filter(parent=None)
    return cats


@register.simple_tag(takes_context=True)
def category_filter_url(context, **kwargs):
    """Category sahifasi uchun filter parametrlari bilan URL qaytaradi."""
    request = context.get('request')
    category = context.get('category')
    if not category:
        return '#'
    if not request:
        return reverse('category_detail', kwargs={'slug': category.slug})
    get = request.GET.copy()
    for key, value in kwargs.items():
        if value is not None and value != '' and str(value).lower() != 'none':
            get[key] = str(value)
        elif key in get:
            del get[key]
    base = reverse('category_detail', kwargs={'slug': category.slug})
    qs = get.urlencode()
    return f"{base}?{qs}" if qs else base









