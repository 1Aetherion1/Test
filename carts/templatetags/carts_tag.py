from django import template
from django.contrib.auth import get_user

from carts.models import Cart
from carts.utils import get_users_carts

register = template.Library()
@register.simple_tag
def users_carts(request):
 return get_users_carts(request)