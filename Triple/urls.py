
from django.urls import path
from django.views.decorators.cache import cache_page

from Triple import views
app_name = 'Triple'
urlpatterns = [
    path('', views.IndexView.as_view(),name='index'),
    path('about/', cache_page(60)(views.AboutView.as_view()),name='about'),
]
