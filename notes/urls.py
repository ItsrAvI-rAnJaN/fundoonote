from django.urls import path
from . import views

urlpatterns = [
    path('notes/', views.NoteAPI.as_view(), name='note_api'),
]