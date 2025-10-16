from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Извлекает значение из словаря по ключу.
    Используется в шаблоне для доступа к годам в range_data.
    """
    return dictionary.get(key)