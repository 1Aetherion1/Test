from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views import View
from django.views.decorators.http import require_POST

from carts.mixin import CartMixin
from carts.models import Cart
from carts.utils import get_users_carts
from goods.models import Products


class CartAddView(CartMixin,View):
    def get_card(self, request, product):
        if request.user.is_authenticated:
            return Cart.objects.filter(
                user=request.user,
                product=product,
            ).first()

        if not request.session.session_key:
            request.session.create()

        return Cart.objects.filter(
            session_key=request.session.session_key,
            product=product,
        ).first()

    def post(self, request):
        product_id = request.POST.get('product_id')
        product = Products.objects.get(id=product_id)

        cart = self.get_card(request, product=product)

        if cart:
            cart.quantity += 1
            cart.save()
        else:
            cart = Cart.objects.create(
                user=(
                    request.user
                    if request.user.is_authenticated
                    else None
                ),
                session_key=(
                    request.session.session_key
                    if not request.user.is_authenticated
                    else None
                ),
                product=product,
                quantity=1,
            )

        users_cart = get_users_carts(request)
        cart_items_html = render_to_string(
            "include/include_cart.html",
            {"carts": users_cart},
            request=request,
        )

        response_data = {
            "message": "Товар добавлен в корзину",
            "cart_items_html": self.render_cart(request)
        }
        return JsonResponse(response_data)



class CartChangeView(CartMixin,View):
    def post(self,request):
        cart_id = request.POST.get('cart_id')

        cart = self.get_cart(request, cart_id = cart_id)
        cart.quantity = request.POST.get('quantity')
        cart.save()

        quantity = cart.quantity

        response_data = {
            'message': 'Количество изменении ',
            'quantity': quantity,
            'cart_items_html': self.render_cart(request)
        }
        return JsonResponse(response_data)


class CartDeleteView(CartMixin,View):
    def post(self,request):
        cart_id = request.POST.get('cart_id')

        cart = self.get_cart(request, cart_id = cart_id)
        quantity = cart.quantity
        cart.delete()

        response_data = {
            'message': 'Товар удален из корзины',
            'quantity': quantity,
            'cart_items_html': self.render_cart(request)

        }
        return JsonResponse(response_data)

