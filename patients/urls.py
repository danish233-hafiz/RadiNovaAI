from django.urls import path
from . import views

urlpatterns = [
    path('', views.patients_list, name='patients_list'),
    path('add/', views.patients_add, name='patients_add'),
    path('<int:pk>/', views.patient_detail, name='patient_detail'),
]
