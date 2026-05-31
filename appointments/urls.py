from django.urls import path
from . import views

urlpatterns = [
    path('', views.appointments_list, name='appointments_list'),
    path('add/', views.appointments_add, name='appointments_add'),
    path('<int:pk>/', views.appointment_detail, name='appointment_detail'),
    path('<int:pk>/edit/', views.appointment_edit, name='appointment_edit'),
    path('<int:pk>/delete/', views.appointment_delete, name='appointment_delete'),
    path('<int:pk>/complete/', views.appointment_complete, name='appointment_complete'),
    path('<int:pk>/cancel/', views.appointment_cancel, name='appointment_cancel'),
    path('<int:pk>/pending/', views.appointment_pending, name='appointment_pending'),
]
