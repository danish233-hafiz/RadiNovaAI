from django.urls import path
from . import views

urlpatterns = [
    path('', views.scans_list, name='scans_list'),
    path('add/', views.scans_add, name='scans_add'),
    path('<int:pk>/', views.scan_detail, name='scan_detail'),
    path('<int:pk>/delete/', views.scan_delete, name='scan_delete'),
]
