from django.shortcuts import render, redirect, get_object_or_404
from .models import ScanRecord
from patients.models import Patient
from appointments.models import Appointment

def scans_list(request):
    scans = ScanRecord.objects.all().order_by('-scan_date')
    return render(request, 'scans_list.html', {'scans': scans})

def scans_add(request):
    if request.method == 'POST':
        scan = ScanRecord.objects.create(
            patient_id=request.POST['patient_id'],
            scan_category=request.POST['scan_category'],
            clinical_notes=request.POST.get('clinical_notes', '')
        )
        if 'scan_image' in request.FILES:
            scan.scan_image = request.FILES['scan_image']
            scan.save()
        return redirect('/radiology/')
    patients = Patient.objects.all()
    appointments = Appointment.objects.all()
    return render(request, 'scans_add.html', {'patients': patients, 'appointments': appointments})

def scan_detail(request, pk):
    scan = get_object_or_404(ScanRecord, pk=pk)
    return render(request, 'scan_detail.html', {'scan': scan})

def scan_delete(request, pk):
    scan = get_object_or_404(ScanRecord, pk=pk)
    if request.method == 'POST':
        scan.delete()
        return redirect('/radiology/')
    return render(request, 'scan_delete.html', {'scan': scan})