from django.urls import path

from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('home/', views.home, name='home'),

    # auth
    path('accounts/loginuser/', views.login_user, name='login-user'),
    path('accounts/register/', views.register, name='register'),
    path('accounts/profile/', views.profile, name='profile'),
]
