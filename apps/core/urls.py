from django.urls import include, path

from core import views

app_name = "core"
urlpatterns = [
    path('', views.DefaultView.as_view(), name='index'),
    path('public-servers/', views.ServerListView.as_view(), name="public-servers"),
    path('manage/', views.ServerManageView.as_view(), name='manage'),
    path('server/add/', views.ServerCreateView.as_view(), name="add"),
    path('server/<int:id>/', include([
        path('share/<int:share_id>/', include([
            path('edit/', views.ServerShareEditView.as_view(), name="share-edit"),
            path('delete/', views.ServerShareDeleteView.as_view(), name="share-delete"),
        ])),
        path('edit/', views.ServerEditView.as_view(), name="edit"),
        path('properties/', views.ServerPropertiesView.as_view(), name="properties"),
        path('permissions/', views.ServerPermissionView.as_view(), name="permissions"),
        path('shares/', views.ServerSharesView.as_view(), name="shares"),
        path('delete/', views.ServerDeleteView.as_view(), name="delete"),
        path('start/', views.ServerStartView.as_view(), name="start"),
        path('stop/', views.ServerStopView.as_view(), name="stop"),
    ])),
]
