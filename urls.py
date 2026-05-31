from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard_router, name='dashboard_router'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/radiographer/', views.radiographer_dashboard, name='radiographer_dashboard'),
    path('dashboard/doctor/', views.doctor_dashboard, name='doctor_dashboard'),
    path('dashboard/receptionist/', views.receptionist_dashboard, name='receptionist_dashboard'),
    path('patient/add/', views.patient_create, name='patient_create'),
    path('appointment/book/', views.appointment_book, name='appointment_book'),
    path('xray/upload/<int:appointment_id>/', views.upload_xray, name='upload_xray'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)