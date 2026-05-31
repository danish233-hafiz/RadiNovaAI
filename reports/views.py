from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Report
from radiology.models import ScanRecord
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def get_ai_suggestion(scan_type, clinical_notes):
    templates = {
        'X-Ray': """Findings:
The chest X-ray demonstrates clear lung fields bilaterally. No evidence of consolidation, pleural effusion, or pneumothorax is identified. The cardiac silhouette is within normal limits. Bony structures appear intact with no acute fractures noted.

Impression:
Normal chest X-ray. Clinical correlation recommended.""",

        'MRI': """Findings:
MRI examination reveals no significant abnormality in the region of interest. Signal intensity appears homogeneous without evidence of mass lesion or pathological enhancement. No restricted diffusion identified.

Impression:
Unremarkable MRI study. Further clinical evaluation advised if symptoms persist.""",

        'CT Scan': """Findings:
CT examination demonstrates no acute intracranial abnormality. No evidence of hemorrhage, infarction, or space-occupying lesion. Visualized bony structures are intact. Soft tissue structures appear within normal limits.

Impression:
Normal CT study. Clinical correlation with patient symptoms recommended.""",

        'Ultrasound': """Findings:
Ultrasound examination reveals normal echotexture of the visualized organs. No abnormal masses, cysts, or fluid collections identified. Vascular flow patterns appear normal on Doppler assessment.

Impression:
Normal ultrasound examination. Follow-up as clinically indicated.""",

        'Mammography': """Findings:
Mammographic examination demonstrates heterogeneously dense breast tissue. No suspicious masses, architectural distortion, or microcalcifications identified. Skin and nipple appear normal bilaterally.

Impression:
No mammographic evidence of malignancy. Routine annual screening recommended.""",

        'Fluoroscopy': """Findings:
Fluoroscopic examination demonstrates normal mucosal pattern without evidence of filling defects or luminal narrowing. Transit time appears within normal limits. No extravasation of contrast medium noted.

Impression:
Normal fluoroscopic study. Clinical correlation recommended.""",
    }
    
    base = templates.get(scan_type, """Findings:
Examination has been performed and reviewed. No acute abnormality identified in the area of clinical concern. Structures appear within normal limits for patient age and clinical presentation.

Impression:
Normal study. Clinical correlation with patient history and symptoms is recommended.""")
    
    if clinical_notes and len(clinical_notes) > 3:
        return f"{base}\n\nClinical Notes Reviewed: {clinical_notes}"
    return base

def reports_list(request):
    reports = Report.objects.all().order_by('-created_at')
    return render(request, 'reports_list.html', {'reports': reports})

def reports_add(request):
    scan_id = request.GET.get('scan_id')
    scan = get_object_or_404(ScanRecord, pk=scan_id)
    ai_suggestion = get_ai_suggestion(scan.scan_category, scan.clinical_notes)
    if request.method == 'POST':
        Report.objects.create(
            scan=scan,
            report_text=request.POST['report_text']
        )
        return redirect('/reports/')
    return render(request, 'reports_add.html', {'scan': scan, 'ai_suggestion': ai_suggestion})

def report_detail(request, pk):
    report = get_object_or_404(Report, pk=pk)
    return render(request, 'report_detail.html', {'report': report})

def report_pdf(request, pk):
    report = get_object_or_404(Report, pk=pk)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="report_{pk}.pdf"'
    p = canvas.Canvas(response, pagesize=letter)
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 750, "RadiNova AI - Medical Report")
    p.setFont("Helvetica", 12)
    p.drawString(100, 710, f"Patient: {report.scan.patient.full_name}")
    p.drawString(100, 690, f"Scan Type: {report.scan.scan_category}")
    p.drawString(100, 670, f"Date: {report.created_at.strftime('%d %b %Y')}")
    p.drawString(100, 640, "Report:")
    y = 620
    for line in report.report_text.split('\n'):
        p.drawString(100, y, line)
        y -= 20
    p.save()
    return response