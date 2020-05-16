from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('public-servers/', views.public_servers, name="public-servers"),
    path('manage/', views.manage, name='manage'),
    path('server/add/', views.add, name="add"),
    path('server/<int:id>/edit/', views.edit, name="edit"),
    path('server/<int:id>/delete/', views.delete, name="delete"),
]
