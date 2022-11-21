from django.urls import path
from . import views

urlpatterns = [
    path('notes/', views.NoteAPI.as_view(), name='note_api'),
    path('collaborator/', views.NotesCollaboratorAPI.as_view(), name='collaborator_api'),
    path('labels/', views.LabelsAPI.as_view(), name='labels_api'),
    path('notes_label/', views.NotesLabelAPI.as_view(), name='notes_label_api'),
]