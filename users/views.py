from django.contrib import auth, messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, TemplateView

from carts.models import Cart
from common.mixin import CacheMixin
from orders.models import Order, OrderItem
from users.forms import (
    UserLoginForm,
    UserRegistrationForm,
    UserProfileForm,
)


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm

    def get_success_url(self):
        return self.get_redirect_url() or reverse_lazy('Triple:index')

    def form_valid(self, form):
        session_key = self.request.session.session_key
        user = form.get_user()

        auth.login(self.request, user)

        if session_key:
            Cart.objects.filter(
                session_key=session_key,
                user__isnull=True,
            ).update(user=user)

        messages.success(
            self.request,
            f'{user.username}, вы вошли в аккаунт!',
        )
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - Авторизация'
        return context


class UserRegistrationView(CreateView):
    template_name = 'users/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('user:profile')

    def form_valid(self, form):
        session_key = self.request.session.session_key

        self.object = form.save()
        user = self.object
        auth.login(self.request, user)

        if session_key:
            Cart.objects.filter(
                session_key=session_key,
                user__isnull=True,
            ).update(user=user)

        messages.success(
            self.request,
            f'{user.username}, вы успешно зарегистрировались '
            'и вошли в аккаунт!',
        )
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - Регистрация'
        return context


class UserProfileView(LoginRequiredMixin, CacheMixin, UpdateView):
    template_name = 'users/profile.html'
    form_class = UserProfileForm
    success_url = reverse_lazy('user:profile')
    login_url = reverse_lazy('user:login')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            'Профиль успешно обновлён',
        )
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - Кабинет'

        orders = (
            Order.objects.filter(users=self.request.user)
            .prefetch_related(
                Prefetch(
                    'orderitem_set',
                    queryset=OrderItem.objects.select_related('product'),
                )
            )
            .order_by('-id')
        )

        context['orders'] = self.set_get_cache(
            orders,
            f'user_{self.request.user.id}_orders',
            60 * 2,
        )
        return context


class UserCartView(TemplateView):
    template_name = 'users/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - Корзина'
        return context


def logout(request):
    auth.logout(request)
    return redirect('Triple:index')