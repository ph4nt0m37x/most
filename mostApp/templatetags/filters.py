from django import template
from mostApp.models import Profile

register = template.Library()

@register.filter
def get_profile_name(user_id):
    return f'{Profile.objects.filter(user_id=user_id).first().first_name} {Profile.objects.filter(user_id=user_id).first().last_name}'
