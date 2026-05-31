from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils import timezone

# =====================================================================
# FEATURE 2: ROLE-BASED ACCESS CONTROL (Custom User Model)
# =====================================================================
class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('radiographer', 'Radiographer'),
        ('doctor', 'Doctor'),
        ('receptionist', 'Receptionist'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='receptionist')

    class Meta:
        app_label = 'RadiNovaAI'

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


# =====================================================================
# FEATURE 3: PATIENT MANAGEMENT MODEL
# =====================================================================
class Patient(models.Model):
    GENDER_CHOICES = (('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other'))
    full_name = models.CharField(max_length=200)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    contact_number = models.CharField(max_length=20)
    address = models.TextField()
    medical_history = models.TextField(blank=True, null=True)
    registered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'RadiNovaAI'

    def __str__(self):
        return self.full_name


# =====================================================================
# FEATURE 4: APPOINTMENT SCHEDULING (With Conflict Detection)
# =====================================================================
class Appointment(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    booked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        app_label = 'RadiNovaAI'

    def clean(self):
        """AUTOMATIC CONFLICT DETECTION: 30 mins overlap handling"""
        if self.appointment_date:
            start_time = self.appointment_date - timezone.timedelta(minutes=29)
            end_time = self.appointment_date + timezone.timedelta(minutes=29)
            overlap = Appointment.objects.filter(
                appointment_date__range=(start_time, end_time),
                status__in=['Pending', 'Confirmed']
            )
            if self.pk:
                overlap = overlap.exclude(pk=self.pk)
            if overlap.exists():
                raise ValidationError({'appointment_date': 'Scheduling Conflict! Is waqt par pehle se appointment booked ha.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.patient.full_name} - {self.appointment_date}"


# =====================================================================
# FEATURE 5: X-RAY MANAGEMENT MODEL
# =====================================================================
class XRayScan(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointment = models.OneToOneField(Appointment, on_delete=models.SET_NULL, null=True, blank=True)
    scan_image = models.ImageField(upload_to='xray_scans/')
    performed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    scan_date = models.DateTimeField(auto_now_add=True)
    clinical_notes = models.TextField(blank=True, null=True)

    class Meta:
        app_label = 'RadiNovaAI'

    def __str__(self):
        return f"X-Ray: {self.patient.full_name}"