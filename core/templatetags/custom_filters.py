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


@register.filter
def calculate_age(birthdate):
    today = datetime.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age


@register.filter
def replace_space(value):
    return value.replace('-', ' ')