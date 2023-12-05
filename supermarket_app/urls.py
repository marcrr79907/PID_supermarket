from django.urls import path, include
from .views import views, product_view, category_view

app_name = 'supermarket'

product_urls = [
    path('product_list/',product_view.ProductListView.as_view() , name='product_list'),
    path('product_create/',product_view.ProductCreateView.as_view() , name='product_create'),
    path('product_update/<int:pk>',product_view.ProductUpdateView.as_view() , name='product_update'),
    path('product_delete/<int:pk>',product_view.ProductDeleteView.as_view() , name='product_delete'),
    path('search_product/',product_view.SearchProductView.as_view() , name='search_product'),
    
]

category_urls = [
    
]

generic_urls = [
    path('', views.IndexView.as_view(), name='index'),
]

urlpatterns = product_urls + category_urls + generic_urls
