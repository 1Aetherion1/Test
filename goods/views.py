from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView

from goods.models import Products, Categories
from goods.utils import q_search


class CatalogView(ListView):
    model = Products
    template_name = 'goods/catalog.html'
    context_object_name = 'goods'
    paginate_by = 3
    allow_empty = True

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        on_sale = self.request.GET.get('on_sale')
        order_by = self.request.GET.get('order_by')
        query = self.request.GET.get('q')

        if query:
            goods = q_search(query)
        elif category_slug == 'all' or category_slug is None:
            goods = super().get_queryset()
        else:
            goods = super().get_queryset().filter(
                category__slug=category_slug
            )
            if not goods.exists():
                raise Http404('Товары не найдены')

        if on_sale:
            goods = goods.filter(discount__gt=0)

        if order_by in ('price', '-price'):
            goods = goods.order_by(order_by, 'id')
        else:
            goods = goods.order_by('id')



        return goods

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - Каталог'
        context['slug_url'] = self.kwargs.get('category_slug', 'all')
        context['categories'] = Categories.objects.all()
        return context


class ProductView(DetailView):
    template_name = 'goods/products.html'
    slug_url_kwarg = 'product_slug'
    context_object_name = 'product'

    def get_object(self, queryset=None):
        return get_object_or_404(
            Products,
            slug=self.kwargs.get(self.slug_url_kwarg),
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        return context