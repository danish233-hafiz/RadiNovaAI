from django.db import models
from radiology.models import ScanRecord

class Report(models.Model):
    scan = models.ForeignKey(ScanRecord, on_delete=models.CASCADE)
    report_text = models.TextField()
    ai_suggestion = models.TextField(blank=True)
    pdf_file = models.FileField(upload_to='reports/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report - {self.scan.patient.full_name} - {self.created_at.date()}"