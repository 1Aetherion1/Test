from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic import FormView

from carts.models import Cart
from goods.models import Products
from orders.forms import CreateOrderForm
from orders.models import Order, OrderItem


class CreateOrderView(LoginRequiredMixin, FormView):
    template_name = 'orders/create_order.html'
    form_class = CreateOrderForm
    success_url = reverse_lazy('user:profile')
    login_url = reverse_lazy('user:login')

    def get_initial(self):
        initial = super().get_initial()
        initial['first_name'] = self.request.user.first_name
        initial['last_name'] = self.request.user.last_name
        initial['requires_delivery'] = '1'
        initial['payment_on_get'] = '0'
        return initial

    def form_valid(self, form):
        try:
            with transaction.atomic():
                user = self.request.user

                cart_items = list(
                    Cart.objects.select_for_update()
                    .filter(user=user)
                    .order_by('product_id', 'id')
                )

                if not cart_items:
                    raise ValidationError('Ваша корзина пуста.')

                order = Order.objects.create(
                    users=user,
                    phone_number=form.cleaned_data['phone_number'],
                    requires_delivery=(
                        form.cleaned_data['requires_delivery'] == '1'
                    ),
                    delivery_address=form.cleaned_data['delivery_address'],
                    payment_on_get=(
                        form.cleaned_data['payment_on_get'] == '1'
                    ),
                )

                for cart_item in cart_items:
                    product = Products.objects.select_for_update().get(
                        id=cart_item.product_id
                    )
                    name = product.name
                    price = product.product_sell_price()
                    quantity = cart_item.quantity

                    if quantity < 1:
                        raise ValidationError(
                            f'У товара «{name}» указано неверное количество.'
                        )

                    if product.quantity < quantity:
                        raise ValidationError(
                            f'Недостаточное количество товара «{name}» '
                            f'на складе. В наличии — {product.quantity}.'
                        )

                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        name=name,
                        price=price,
                        quantity=quantity,
                    )

                    product.quantity -= quantity
                    product.save(update_fields=['quantity'])

                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.save(update_fields=['first_name', 'last_name'])

                Cart.objects.filter(
                    user=user,
                    id__in=[item.id for item in cart_items],
                ).delete()

        except ValidationError as error:
            form.add_error(None, error)
            return self.form_invalid(form)

        messages.success(self.request, 'Заказ оформлен!')
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Оформление заказа'
        context['order'] = True
        return context