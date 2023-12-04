from django.urls import path
from .views import UsersLoginView, LogoutView, RegisterView

app_name = 'users'

urlpatterns = [
    path('login/',UsersLoginView.as_view() , name='login'),
    path('register/', RegisterView.as_view() , name='register'),
    path('logout/',LogoutView.as_view() , name='logout'),
]