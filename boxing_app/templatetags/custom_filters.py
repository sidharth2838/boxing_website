from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    """Multiply the value by the argument"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0
    
@register.filter
def multiply(value, arg):
    """Multiply the value by the argument"""
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        return value

@register.filter
def add(value, arg):
    """Add the value to the argument"""
    try:
        return int(value) + int(arg)
    except (ValueError, TypeError):
        return value
    


from django import template

register = template.Library()

@register.filter
def sum_values(values):
    """Sum all values in a dictionary"""
    return sum(values.values())    