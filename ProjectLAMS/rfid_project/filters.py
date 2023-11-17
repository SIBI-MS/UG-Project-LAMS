from django import template
from datetime import timedelta

register = template.Library()

@register.filter(name='timeformat')
def timeformat(seconds):
    # Convert the total_seconds (seconds) to a timedelta object
    total_time = timedelta(seconds=seconds)

    # Extract the hours, minutes, and seconds from the timedelta
    hours = total_time.seconds // 3600
    minutes = (total_time.seconds % 3600) // 60
    seconds = total_time.seconds % 60

    # Format the time as HH:MM:SS
    return f'{hours:02d}:{minutes:02d}:{seconds:02d}'
