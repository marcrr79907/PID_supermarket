from django.urls import path, include
from .views import views, product_view, category_view

app_name = 'supermarket'

product_urls = [
    path('product/',product_view.ProductListView.as_view() , name='product_list')
]

category_urls = []

generic_urls = [
    path('', views.IndexView.as_view(), name='index'),
    path('main/',views.MainView.as_view() , name='main')
]

urlpatterns = product_urls + category_urls + generic_urls
