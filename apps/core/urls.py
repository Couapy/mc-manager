from django.urls import path

from . import views


app_name = "core"
urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('public-servers/', views.public_servers, name="public-servers"),
    path('manage/', views.manage, name='manage'),
    path('server/add/', views.add, name="add"),
    path('server/<int:id>/edit/', views.edit, name="edit"),
    path('server/<int:id>/properties/', views.properties, name="properties"),
    path('server/<int:id>/permissions/', views.permissions, name="permissions"),
    path('server/<int:id>/delete/', views.delete, name="delete"),
    path('server/<int:id>/start/', views.start, name="start"),
    path('server/<int:id>/stop/', views.stop, name="stop"),
]
