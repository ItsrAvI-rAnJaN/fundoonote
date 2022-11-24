from django.urls import path
from . import views

urlpatterns = [
    path('registration/', views.Register.as_view() , name='registration'),
    path('loginapi/', views.Login.as_view(), name='loginapi'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
]
