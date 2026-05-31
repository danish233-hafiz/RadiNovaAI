from django.shortcuts import render, redirect, get_object_or_404
from .models import Patient

def patients_list(request):
    query = request.GET.get('q', '')
    if query:
        patients = Patient.objects.filter(full_name__icontains=query)
    else:
        patients = Patient.objects.all().order_by('-created_at')
    return render(request, 'patients_list.html', {'patients': patients})

def patients_add(request):
    if request.method == 'POST':
        Patient.objects.create(
            full_name=request.POST['full_name'],
            date_of_birth=request.POST['date_of_birth'],
            gender=request.POST['gender'],
            contact_number=request.POST['contact_number'],
            medical_history=request.POST.get('medical_history', '')
        )
        return redirect('/patients/')
    return render(request, 'patients_add.html')

def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    return render(request, 'patient_detail.html', {'patient': patient})

def patient_edit(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        patient.full_name = request.POST['full_name']
        patient.date_of_birth = request.POST['date_of_birth']
        patient.gender = request.POST['gender']
        patient.contact_number = request.POST['contact_number']
        patient.medical_history = request.POST.get('medical_history', '')
        patient.save()
        return redirect(f'/patients/{pk}/')
    return render(request, 'patient_edit.html', {'patient': patient})

def patient_delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        patient.delete()
        return redirect('/patients/')
    return render(request, 'patient_delete.html', {'patient': patient})