from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('insertion', views.insertion, name='index'),
    path('extraction', views.extraction, name='index'),
    path('download/<str:io>/<str:filetype>/<str:filename>', views.download, name='index'),
]