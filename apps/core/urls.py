from django.urls import include, path

from core import views

app_name = "core"
urlpatterns = [
    path('', views.DefaultView.as_view(), name='index'),
    path('public-servers/', views.ServerListView.as_view(), name="public-servers"),
    path('manage/', views.ServerManageView.as_view(), name='manage'),
    path('server/', include([
        path('add/', views.ServerCreateView.as_view(), name="add"),
        path('<int:id>/edit/', views.ServerEditView.as_view(), name="edit"),
        path('<int:id>/properties/', views.ServerPropertiesView.as_view(), name="properties"),
        path('<int:id>/permissions/', views.ServerPermissionView.as_view(), name="permissions"),
        path('<int:id>/delete/', views.ServerDeleteView.as_view(), name="delete"),
        path('<int:id>/start/', views.ServerStartView.as_view(), name="start"),
        path('<int:id>/stop/', views.ServerStopView.as_view(), name="stop"),
    ])),
]
