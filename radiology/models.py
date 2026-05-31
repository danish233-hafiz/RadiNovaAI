from django.db import models
from patients.models import Patient
from appointments.models import Appointment

class ScanRecord(models.Model):
    SCAN_CHOICES = [
        ('X-Ray', 'X-Ray'),
        ('Ultrasound', 'Ultrasound'),
    ]
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment, on_delete=models.SET_NULL, null=True, blank=True)
    scan_category = models.CharField(max_length=50, choices=SCAN_CHOICES)
    scan_image = models.ImageField(upload_to='scans/', blank=True, null=True)
    clinical_notes = models.TextField(blank=True)
    scan_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.full_name} - {self.scan_category}"