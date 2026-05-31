from django.urls import path
from . import views

urlpatterns = [
    path('', views.reports_list, name='reports_list'),
    path('add/', views.reports_add, name='reports_add'),
    path('<int:pk>/', views.report_detail, name='report_detail'),
    path('<int:pk>/pdf/', views.report_pdf, name='report_pdf'),
]
