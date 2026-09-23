from django.template.loader import render_to_string
from django.urls import reverse

from carts.models import Cart
from carts.utils import get_users_carts


class CartMixin:
    def get_cart(self, request, product=None, cart_id=None):
        if request.user.is_authenticated:
            query_kwargs = {'user': request.user}
        else:
            if not request.session.session_key:
                request.session.create()

            query_kwargs = {
                'session_key': request.session.session_key,
            }

        if product is not None:
            query_kwargs['product'] = product

        if cart_id is not None:
            query_kwargs['id'] = cart_id

        return Cart.objects.filter(**query_kwargs).first()

    def render_cart(self, request):
        users_cart = get_users_carts(request)
        context = {'carts': users_cart}

        referer = request.META.get('HTTP_REFERER', '')
        if reverse('orders:create_order') in referer:
            context['order'] = True

        return render_to_string(
            'include/include_cart.html',
            context,
            request=request,
        )