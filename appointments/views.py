from django.shortcuts import render, redirect, get_object_or_404
from .models import Appointment
from patients.models import Patient

def appointments_list(request):
    query = request.GET.get('q', '')
    payment_filter = request.GET.get('payment', '')
    status_filter = request.GET.get('status', '')

    appointments = Appointment.objects.all().order_by('-appointment_date')

    if query:
        appointments = appointments.filter(patient__full_name__icontains=query)
    if payment_filter:
        appointments = appointments.filter(payment_status=payment_filter)
    if status_filter:
        appointments = appointments.filter(status=status_filter)

    context = {
        'appointments': appointments,
        'paid': Appointment.objects.filter(payment_status='Paid').count(),
        'unpaid': Appointment.objects.filter(payment_status='Unpaid').count(),
        'pending': Appointment.objects.filter(status='Pending').count(),
        'completed': Appointment.objects.filter(status='Completed').count(),
        'cancelled': Appointment.objects.filter(status='Cancelled').count(),
    }
    return render(request, 'appointments_list.html', context)

def appointments_add(request):
    if request.method == 'POST':
        Appointment.objects.create(
            patient_id=request.POST['patient_id'],
            scan_type=request.POST['scan_type'],
            appointment_date=request.POST['appointment_date'],
            notes=request.POST.get('notes', '')
        )
        return redirect('/appointments/')
    patients = Patient.objects.all()
    return render(request, 'appointments_add.html', {'patients': patients})
    
def appointment_detail(request, pk):
    appt = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'mark_paid':
            appt.payment_status = 'Paid'
        elif action == 'mark_unpaid':
            appt.payment_status = 'Unpaid'
        elif action == 'complete':
            appt.status = 'Completed'
        elif action == 'cancel':
            appt.status = 'Cancelled'
        elif action == 'pending':
            appt.status = 'Pending'
        elif action == 'set_fees':
            appt.fees = request.POST.get('fees', 0)
        appt.save()
        return redirect(f'/appointments/{pk}/')
    return render(request, 'appointment_detail.html', {'appt': appt})

def appointment_edit(request, pk):
    appt = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        appt.patient_id = request.POST['patient_id']
        appt.scan_type = request.POST['scan_type']
        appt.appointment_date = request.POST['appointment_date']
        appt.notes = request.POST.get('notes', '')
        appt.save()
        return redirect(f'/appointments/{pk}/')
    patients = Patient.objects.all()
    return render(request, 'appointments_add.html', {'appt': appt, 'patients': patients})

def appointment_delete(request, pk):
    appt = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        appt.delete()
        return redirect('/appointments/')
    return render(request, 'appointment_delete.html', {'appt': appt})

def appointment_complete(request, pk):
    appt = get_object_or_404(Appointment, pk=pk)
    appt.status = 'Completed'
    appt.save()
    return redirect('/appointments/')

def appointment_cancel(request, pk):
    appt = get_object_or_404(Appointment, pk=pk)
    appt.status = 'Cancelled'
    appt.save()
    return redirect('/appointments/')

def appointment_pending(request, pk):
    appt = get_object_or_404(Appointment, pk=pk)
    appt.status = 'Pending'
    appt.save()
    return redirect('/appointments/')