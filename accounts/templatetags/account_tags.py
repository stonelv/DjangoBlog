from django import template
from django.contrib.auth.models import AnonymousUser

from accounts.models import BlogUser

register = template.Library()


@register.simple_tag(takes_context=True)
def unread_notifications_count(context):
    """
    获取当前用户未读通知数量
    """
    request = context.get('request')
    if request and hasattr(request, 'user') and request.user.is_authenticated and isinstance(request.user, BlogUser):
        return request.user.get_unread_notifications_count()
    return 0