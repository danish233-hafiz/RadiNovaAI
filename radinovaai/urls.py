from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render, redirect
from django.conf import settings
from django.conf.urls.static import static
from patients.models import Patient
from appointments.models import Appointment
from radiology.models import ScanRecord
from reports.models import Report
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login

@login_required
def dashboard(request):
    scan_types = ['X-Ray', 'MRI', 'CT Scan', 'Ultrasound', 'Mammography', 'Fluoroscopy']
    scan_counts = [ScanRecord.objects.filter(scan_category=s).count() for s in scan_types]
    status_counts = [
        Appointment.objects.filter(status='Pending').count(),
        Appointment.objects.filter(status='Completed').count(),
        Appointment.objects.filter(status='Cancelled').count(),
    ]
    context = {
        'total_patients': Patient.objects.count(),
        'total_appointments': Appointment.objects.count(),
        'total_scans': ScanRecord.objects.count(),
        'total_reports': Report.objects.count(),
        'scan_counts': scan_counts,
        'status_counts': status_counts,
        'recent_patients': Patient.objects.all().order_by('-created_at')[:5],
    }
    return render(request, 'dashboard.html', context)

def custom_logout(request):
    logout(request)
    return redirect('/login/')

def custom_login(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    error = None
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            return redirect('/dashboard/')
        else:
            error = 'Username ya password galat hai!'
    return render(request, 'login.html', {'error': error})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', custom_login, name='login'),
    path('logout/', custom_logout, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('register/', include('users.urls')),
    path('patients/', include('patients.urls')),
    path('appointments/', include('appointments.urls')),
    path('radiology/', include('radiology.urls')),
    path('reports/', include('reports.urls')),
    path('accounts/login/', lambda request: redirect('/login/')),
    path('', lambda request: redirect('/dashboard/')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)