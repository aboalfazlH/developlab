from django import template

register = template.Library()

@register.filter
def is_following(user, target_user):
    return user.following.filter(id=target_user.id).exists()