from django.urls import path

from . import views

urlpatterns = [
    path('', views.profile, name='index'),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('profile/', views.profile, name='profile'),
]
