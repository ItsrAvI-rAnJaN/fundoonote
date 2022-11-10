from django.urls import path,include
from . import views

urlpatterns = [
    path('registration/', views.Register.as_view() , name='registration'),
    path('loginapi/', views.Login.as_view(), name='loginapi'),
]
