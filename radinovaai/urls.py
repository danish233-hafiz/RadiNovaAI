from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from users import views as views_users

from radinovaai.views import custom_login, custom_logout, dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', custom_login, name='login'),
    path('logout/', custom_logout, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('register/', views_users.register, name='register'),
    path('patients/', include('patients.urls')),
    path('appointments/', include('appointments.urls')),
    path('radiology/', include('radiology.urls')),
    path('reports/', include('reports.urls')),
    path('accounts/login/', lambda request: redirect('/login/')),
    path('', lambda request: redirect('/dashboard/')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)