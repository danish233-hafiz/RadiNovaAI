from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import Patient, Appointment, XRayScan

def check_role(user, role_name):
    return user.is_authenticated and (user.role == role_name or user.role == 'admin')

@login_required
def dashboard_router(request):
    if request.user.role == 'admin': return redirect('admin_dashboard')
    elif request.user.role == 'radiographer': return redirect('radiographer_dashboard')
    elif request.user.role == 'doctor': return redirect('doctor_dashboard')
    return redirect('receptionist_dashboard')

@login_required
def admin_dashboard(request):
    if request.user.role != 'admin': return HttpResponseForbidden("Access Denied")
    return render(request, 'dashboards/admin.html', {'tp': Patient.objects.count(), 'ta': Appointment.objects.count(), 'tx': XRayScan.objects.count()})

@login_required
def radiographer_dashboard(request):
    if not check_role(request.user, 'radiographer'): return HttpResponseForbidden()
    return render(request, 'dashboards/radiographer.html', {'pending': Appointment.objects.filter(status='Confirmed'), 'completed': XRayScan.objects.all()})

@login_required
def doctor_dashboard(request):
    if not check_role(request.user, 'doctor'): return HttpResponseForbidden()
    return render(request, 'dashboards/doctor.html', {'xrays': XRayScan.objects.all()})

@login_required
def receptionist_dashboard(request):
    if not check_role(request.user, 'receptionist'): return HttpResponseForbidden()
    return render(request, 'dashboards/receptionist.html', {'patients': Patient.objects.all()[:10], 'appointments': Appointment.objects.filter(status='Pending')})

@login_required
def patient_create(request):
    if not check_role(request.user, 'receptionist'): return HttpResponseForbidden()
    if request.method == 'POST':
        Patient.objects.create(
            full_name=request.POST.get('full_name'), date_of_birth=request.POST.get('date_of_birth'),
            gender=request.POST.get('gender'), contact_number=request.POST.get('contact_number'),
            address=request.POST.get('address'), medical_history=request.POST.get('medical_history'), registered_by=request.user
        )
        messages.success(request, "Patient Profile Created successfully!")
        return redirect('receptionist_dashboard')
    return render(request, 'patients/patient_form.html')

@login_required
def appointment_book(request):
    if not check_role(request.user, 'receptionist'): return HttpResponseForbidden()
    if request.method == 'POST':
        try:
            p = get_object_or_404(Patient, id=request.POST.get('patient'))
            app = Appointment(patient=p, appointment_date=request.POST.get('appointment_date'), notes=request.POST.get('notes'), booked_by=request.user)
            app.save()
            messages.success(request, "Appointment Booked!")
            return redirect('receptionist_dashboard')
        except Exception:
            messages.error(request, "Conflict detected! Select another time slot.")
    return render(request, 'appointments/book_form.html', {'patients': Patient.objects.all()})

@login_required
def upload_xray(request, appointment_id):
    if not check_role(request.user, 'radiographer'): return HttpResponseForbidden()
    app = get_object_or_404(Appointment, id=appointment_id)
    if request.method == 'POST' and request.FILES.get('scan_image'):
        XRayScan.objects.create(patient=app.patient, appointment=app, scan_image=request.FILES.get('scan_image'), performed_by=request.user, clinical_notes=request.POST.get('clinical_notes'))
        app.status = 'Completed'
        app.save()
        messages.success(request, "X-Ray Uploaded Successfully!")
        return redirect('radiographer_dashboard')
    return render(request, 'radiology/upload_form.html', {'appointment': app})