from django import template
from datetime import datetime, time, timedelta

register = template.Library()

@register.filter
def add_minutes(value, minutes):
    if type(value) == str and value:
        value = datetime.strptime(value, "%H:%M").time()

    if isinstance(value, time):
        current_datetime = datetime.now()
        value_datetime = datetime.combine(current_datetime.date(), value)
        new_datetime = value_datetime + timedelta(minutes=int(minutes))
        return new_datetime.time()

    return value