base = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>RadiNova AI</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css" rel="stylesheet">
<style>
body{background:#f0f4f8}
.sidebar{min-height:100vh;background:#1e3a5f}
.sidebar a{color:#cce0ff;text-decoration:none;display:block;padding:10px 20px}
.sidebar a:hover{background:#2563eb;color:white}
.sidebar .brand{color:white;font-size:1.4rem;font-weight:bold;padding:20px;border-bottom:1px solid #2563eb}
.main-content{padding:30px}
.navbar-top{background:white;border-bottom:2px solid #e5e7eb;padding:10px 20px}
</style>
</head>
<body>
<div class="container-fluid">
<div class="row">
<div class="col-md-2 sidebar p-0">
<div class="brand">RadiNova AI</div>
<a href="/dashboard/">Dashboard</a>
<a href="/patients/">Patients</a>
<a href="/appointments/">Appointments</a>
<a href="/radiology/">Scans</a>
<a href="/reports/">Reports</a>
<a href="/logout/">Logout</a>
</div>
<div class="col-md-10 p-0">
<div class="navbar-top"><span class="fw-bold text-primary">Welcome, {{ request.user.username }}</span></div>
<div class="main-content">{% block content %}{% endblock %}</div>
</div>
</div>
</div>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>"""

dashboard = """{% extends 'base.html' %}
{% block content %}
<h2 class="mb-4">Dashboard</h2>
<div class="row">
<div class="col-md-3">
<div class="card text-white bg-primary mb-3">
<div class="card-body">
<h5 class="card-title">Total Patients</h5>
<h2>{{ total_patients }}</h2>
</div>
</div>
</div>
<div class="col-md-3">
<div class="card text-white bg-success mb-3">
<div class="card-body">
<h5 class="card-title">Appointments</h5>
<h2>{{ total_appointments }}</h2>
</div>
</div>
</div>
<div class="col-md-3">
<div class="card text-white bg-warning mb-3">
<div class="card-body">
<h5 class="card-title">Scans</h5>
<h2>{{ total_scans }}</h2>
</div>
</div>
</div>
<div class="col-md-3">
<div class="card text-white bg-danger mb-3">
<div class="card-body">
<h5 class="card-title">Reports</h5>
<h2>{{ total_reports }}</h2>
</div>
</div>
</div>
</div>
{% endblock %}"""

open('templates/base.html', 'w', encoding='utf-8').write(base)
open('templates/dashboard.html', 'w', encoding='utf-8').write(dashboard)
print('Done!')
patients_list = """{% extends 'base.html' %}
{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
<h2>Patients</h2>
<a href="/patients/add/" class="btn btn-primary">+ Add Patient</a>
</div>
<div class="card">
<div class="card-body">
<table class="table table-hover">
<thead class="table-dark">
<tr><th>Name</th><th>Gender</th><th>Contact</th><th>Registered</th><th>Action</th></tr>
</thead>
<tbody>
{% for patient in patients %}
<tr>
<td>{{ patient.full_name }}</td>
<td>{{ patient.gender }}</td>
<td>{{ patient.contact_number }}</td>
<td>{{ patient.created_at|date:"d M Y" }}</td>
<td><a href="/patients/{{ patient.id }}/" class="btn btn-sm btn-info">View</a></td>
</tr>
{% empty %}
<tr><td colspan="5" class="text-center">No patients found</td></tr>
{% endfor %}
</tbody>
</table>
</div>
</div>
{% endblock %}"""

patients_add = """{% extends 'base.html' %}
{% block content %}
<h2 class="mb-4">Add New Patient</h2>
<div class="card" style="max-width:600px">
<div class="card-body">
<form method="post">
{% csrf_token %}
<div class="mb-3"><label class="form-label">Full Name</label><input type="text" name="full_name" class="form-control" required></div>
<div class="mb-3"><label class="form-label">Date of Birth</label><input type="date" name="date_of_birth" class="form-control" required></div>
<div class="mb-3"><label class="form-label">Gender</label>
<select name="gender" class="form-control">
<option>Male</option><option>Female</option><option>Other</option>
</select></div>
<div class="mb-3"><label class="form-label">Contact Number</label><input type="text" name="contact_number" class="form-control" required></div>
<div class="mb-3"><label class="form-label">Medical History</label><textarea name="medical_history" class="form-control" rows="3"></textarea></div>
<button type="submit" class="btn btn-primary">Save Patient</button>
<a href="/patients/" class="btn btn-secondary">Cancel</a>
</form>
</div>
</div>
{% endblock %}"""

patient_detail = """{% extends 'base.html' %}
{% block content %}
<h2 class="mb-4">Patient Detail</h2>
<div class="card" style="max-width:600px">
<div class="card-body">
<p><strong>Name:</strong> {{ patient.full_name }}</p>
<p><strong>Date of Birth:</strong> {{ patient.date_of_birth }}</p>
<p><strong>Gender:</strong> {{ patient.gender }}</p>
<p><strong>Contact:</strong> {{ patient.contact_number }}</p>
<p><strong>Medical History:</strong> {{ patient.medical_history }}</p>
<p><strong>Registered:</strong> {{ patient.created_at|date:"d M Y" }}</p>
<a href="/patients/" class="btn btn-secondary">Back</a>
</div>
</div>
{% endblock %}"""

open('templates/patients_list.html', 'w', encoding='utf-8').write(patients_list)
open('templates/patients_add.html', 'w', encoding='utf-8').write(patients_add)
open('templates/patient_detail.html', 'w', encoding='utf-8').write(patient_detail)
print('Patients templates done!')
open('patients/urls.py','w',encoding='utf-8').write("""from django.urls import path
from . import views

urlpatterns = [
    path('', views.patients_list, name='patients_list'),
    path('add/', views.patients_add, name='patients_add'),
    path('<int:pk>/', views.patient_detail, name='patient_detail'),
]
""")
print('patients urls done!')
# Appointments urls
open('appointments/urls.py','w',encoding='utf-8').write(
"from django.urls import path\nfrom . import views\n\nurlpatterns = [\n    path('', views.appointments_list, name='appointments_list'),\n    path('add/', views.appointments_add, name='appointments_add'),\n    path('<int:pk>/', views.appointment_detail, name='appointment_detail'),\n]\n"
)

# Appointments templates
al = open('templates/appointments_list.html','w',encoding='utf-8')
al.write("{% extends 'base.html' %}\n{% block content %}\n<div class='d-flex justify-content-between align-items-center mb-4'>\n<h2>Appointments</h2>\n<a href='/appointments/add/' class='btn btn-primary'>+ New Appointment</a>\n</div>\n<div class='card'><div class='card-body'>\n<table class='table table-hover'>\n<thead class='table-dark'><tr><th>Patient</th><th>Scan Type</th><th>Date</th><th>Status</th><th>Action</th></tr></thead>\n<tbody>\n{% for appt in appointments %}\n<tr>\n<td>{{ appt.patient.full_name }}</td>\n<td>{{ appt.scan_type }}</td>\n<td>{{ appt.appointment_date|date:'d M Y H:i' }}</td>\n<td><span class='badge bg-warning'>{{ appt.status }}</span></td>\n<td><a href='/appointments/{{ appt.id }}/' class='btn btn-sm btn-info'>View</a></td>\n</tr>\n{% empty %}\n<tr><td colspan='5' class='text-center'>No appointments</td></tr>\n{% endfor %}\n</tbody></table>\n</div></div>\n{% endblock %}")
al.close()

aa = open('templates/appointments_add.html','w',encoding='utf-8')
aa.write("{% extends 'base.html' %}\n{% block content %}\n<h2 class='mb-4'>New Appointment</h2>\n<div class='card' style='max-width:600px'><div class='card-body'>\n<form method='post'>\n{% csrf_token %}\n<div class='mb-3'><label class='form-label'>Patient</label>\n<select name='patient_id' class='form-control' required>\n{% for patient in patients %}\n<option value='{{ patient.id }}'>{{ patient.full_name }}</option>\n{% endfor %}\n</select></div>\n<div class='mb-3'><label class='form-label'>Scan Type</label>\n<select name='scan_type' class='form-control'><option>X-Ray</option><option>Ultrasound</option></select></div>\n<div class='mb-3'><label class='form-label'>Date and Time</label>\n<input type='datetime-local' name='appointment_date' class='form-control' required></div>\n<div class='mb-3'><label class='form-label'>Notes</label>\n<textarea name='notes' class='form-control' rows='3'></textarea></div>\n<button type='submit' class='btn btn-primary'>Save</button>\n<a href='/appointments/' class='btn btn-secondary'>Cancel</a>\n</form></div></div>\n{% endblock %}")
aa.close()

ad = open('templates/appointment_detail.html','w',encoding='utf-8')
ad.write("{% extends 'base.html' %}\n{% block content %}\n<h2 class='mb-4'>Appointment Detail</h2>\n<div class='card' style='max-width:600px'><div class='card-body'>\n<p><strong>Patient:</strong> {{ appt.patient.full_name }}</p>\n<p><strong>Scan Type:</strong> {{ appt.scan_type }}</p>\n<p><strong>Date:</strong> {{ appt.appointment_date|date:'d M Y H:i' }}</p>\n<p><strong>Status:</strong> {{ appt.status }}</p>\n<p><strong>Notes:</strong> {{ appt.notes }}</p>\n<a href='/appointments/' class='btn btn-secondary'>Back</a>\n</div></div>\n{% endblock %}")
ad.close()

print('Appointments done!')
# Update appointments_add with more scan types
aa2 = open('templates/appointments_add.html','w',encoding='utf-8')
aa2.write("{% extends 'base.html' %}\n{% block content %}\n<h2 class='mb-4'>New Appointment</h2>\n<div class='card' style='max-width:600px'><div class='card-body'>\n<form method='post'>\n{% csrf_token %}\n<div class='mb-3'><label class='form-label'>Patient</label>\n<select name='patient_id' class='form-control' required>\n{% for patient in patients %}\n<option value='{{ patient.id }}'>{{ patient.full_name }}</option>\n{% endfor %}\n</select></div>\n<div class='mb-3'><label class='form-label'>Scan Type</label>\n<select name='scan_type' class='form-control'>\n<option>X-Ray</option>\n<option>Ultrasound</option>\n<option>MRI</option>\n<option>CT Scan</option>\n<option>Mammography</option>\n<option>Fluoroscopy</option>\n</select></div>\n<div class='mb-3'><label class='form-label'>Date and Time</label>\n<input type='datetime-local' name='appointment_date' class='form-control' required></div>\n<div class='mb-3'><label class='form-label'>Notes</label>\n<textarea name='notes' class='form-control' rows='3'></textarea></div>\n<button type='submit' class='btn btn-primary'>Save</button>\n<a href='/appointments/' class='btn btn-secondary'>Cancel</a>\n</form></div></div>\n{% endblock %}")
aa2.close()
print('Scan types updated!')
# Radiology urls
open('radiology/urls.py','w',encoding='utf-8').write(
"from django.urls import path\nfrom . import views\n\nurlpatterns = [\n    path('', views.scans_list, name='scans_list'),\n    path('add/', views.scans_add, name='scans_add'),\n    path('<int:pk>/', views.scan_detail, name='scan_detail'),\n]\n"
)

sl = open('templates/scans_list.html','w',encoding='utf-8')
sl.write("{% extends 'base.html' %}\n{% block content %}\n<div class='d-flex justify-content-between align-items-center mb-4'>\n<h2>Scan Records</h2>\n<a href='/radiology/add/' class='btn btn-primary'>+ New Scan</a>\n</div>\n<div class='card'><div class='card-body'>\n<table class='table table-hover'>\n<thead class='table-dark'><tr><th>Patient</th><th>Scan Type</th><th>Date</th><th>Action</th></tr></thead>\n<tbody>\n{% for scan in scans %}\n<tr>\n<td>{{ scan.patient.full_name }}</td>\n<td>{{ scan.scan_category }}</td>\n<td>{{ scan.scan_date|date:'d M Y' }}</td>\n<td><a href='/radiology/{{ scan.id }}/' class='btn btn-sm btn-info'>View</a></td>\n</tr>\n{% empty %}\n<tr><td colspan='4' class='text-center'>No scans found</td></tr>\n{% endfor %}\n</tbody></table>\n</div></div>\n{% endblock %}")
sl.close()

sa = open('templates/scans_add.html','w',encoding='utf-8')
sa.write("{% extends 'base.html' %}\n{% block content %}\n<h2 class='mb-4'>New Scan Record</h2>\n<div class='card' style='max-width:600px'><div class='card-body'>\n<form method='post' enctype='multipart/form-data'>\n{% csrf_token %}\n<div class='mb-3'><label class='form-label'>Patient</label>\n<select name='patient_id' class='form-control' required>\n{% for patient in patients %}\n<option value='{{ patient.id }}'>{{ patient.full_name }}</option>\n{% endfor %}\n</select></div>\n<div class='mb-3'><label class='form-label'>Scan Type</label>\n<select name='scan_category' class='form-control'>\n<option>X-Ray</option><option>Ultrasound</option><option>MRI</option><option>CT Scan</option><option>Mammography</option><option>Fluoroscopy</option>\n</select></div>\n<div class='mb-3'><label class='form-label'>Scan Image</label>\n<input type='file' name='scan_image' class='form-control' accept='image/*'></div>\n<div class='mb-3'><label class='form-label'>Clinical Notes</label>\n<textarea name='clinical_notes' class='form-control' rows='3'></textarea></div>\n<button type='submit' class='btn btn-primary'>Save</button>\n<a href='/radiology/' class='btn btn-secondary'>Cancel</a>\n</form></div></div>\n{% endblock %}")
sa.close()

sd = open('templates/scan_detail.html','w',encoding='utf-8')
sd.write("{% extends 'base.html' %}\n{% block content %}\n<h2 class='mb-4'>Scan Detail</h2>\n<div class='card' style='max-width:600px'><div class='card-body'>\n<p><strong>Patient:</strong> {{ scan.patient.full_name }}</p>\n<p><strong>Scan Type:</strong> {{ scan.scan_category }}</p>\n<p><strong>Date:</strong> {{ scan.scan_date|date:'d M Y' }}</p>\n<p><strong>Clinical Notes:</strong> {{ scan.clinical_notes }}</p>\n{% if scan.scan_image %}\n<p><strong>Scan Image:</strong></p>\n<img src='{{ scan.scan_image.url }}' style='max-width:100%;border-radius:8px;'>\n{% endif %}\n<br><br>\n<a href='/radiology/' class='btn btn-secondary'>Back</a>\n<a href='/reports/add/?scan_id={{ scan.id }}' class='btn btn-success'>Create Report</a>\n</div></div>\n{% endblock %}")
sd.close()

print('Radiology done!')
# Reports urls
open('reports/urls.py','w',encoding='utf-8').write(
"from django.urls import path\nfrom . import views\n\nurlpatterns = [\n    path('', views.reports_list, name='reports_list'),\n    path('add/', views.reports_add, name='reports_add'),\n    path('<int:pk>/', views.report_detail, name='report_detail'),\n    path('<int:pk>/pdf/', views.report_pdf, name='report_pdf'),\n]\n"
)

rl = open('templates/reports_list.html','w',encoding='utf-8')
rl.write("{% extends 'base.html' %}\n{% block content %}\n<div class='d-flex justify-content-between align-items-center mb-4'>\n<h2>Reports</h2>\n</div>\n<div class='card'><div class='card-body'>\n<table class='table table-hover'>\n<thead class='table-dark'><tr><th>Patient</th><th>Scan Type</th><th>Date</th><th>Action</th></tr></thead>\n<tbody>\n{% for report in reports %}\n<tr>\n<td>{{ report.scan.patient.full_name }}</td>\n<td>{{ report.scan.scan_category }}</td>\n<td>{{ report.created_at|date:'d M Y' }}</td>\n<td><a href='/reports/{{ report.id }}/' class='btn btn-sm btn-info'>View</a></td>\n</tr>\n{% empty %}\n<tr><td colspan='4' class='text-center'>No reports found</td></tr>\n{% endfor %}\n</tbody></table>\n</div></div>\n{% endblock %}")
rl.close()

ra = open('templates/reports_add.html','w',encoding='utf-8')
ra.write("{% extends 'base.html' %}\n{% block content %}\n<h2 class='mb-4'>Create Report</h2>\n<div class='card' style='max-width:700px'><div class='card-body'>\n<p><strong>Patient:</strong> {{ scan.patient.full_name }}</p>\n<p><strong>Scan Type:</strong> {{ scan.scan_category }}</p>\n<form method='post'>\n{% csrf_token %}\n<div class='mb-3'><label class='form-label'>Report Text</label>\n<textarea name='report_text' class='form-control' rows='5' required></textarea></div>\n<button type='submit' class='btn btn-success'>Save Report</button>\n<a href='/radiology/' class='btn btn-secondary'>Cancel</a>\n</form></div></div>\n{% endblock %}")
ra.close()

rd = open('templates/report_detail.html','w',encoding='utf-8')
rd.write("{% extends 'base.html' %}\n{% block content %}\n<h2 class='mb-4'>Report Detail</h2>\n<div class='card' style='max-width:700px'><div class='card-body'>\n<p><strong>Patient:</strong> {{ report.scan.patient.full_name }}</p>\n<p><strong>Scan Type:</strong> {{ report.scan.scan_category }}</p>\n<p><strong>Date:</strong> {{ report.created_at|date:'d M Y' }}</p>\n<hr>\n<p><strong>Report:</strong></p>\n<p>{{ report.report_text }}</p>\n<a href='/reports/{{ report.id }}/pdf/' class='btn btn-danger'>Download PDF</a>\n<a href='/reports/' class='btn btn-secondary'>Back</a>\n</div></div>\n{% endblock %}")
rd.close()

print('Reports templates done!')
login_page = open('templates/login.html','w',encoding='utf-8')
login_page.write("<!DOCTYPE html>\n<html>\n<head>\n<meta charset='UTF-8'>\n<title>RadiNova AI - Login</title>\n<link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css' rel='stylesheet'>\n<style>\nbody{background:linear-gradient(135deg,#1e3a5f,#2563eb);min-height:100vh;display:flex;align-items:center;justify-content:center;}\n.card{border-radius:15px;box-shadow:0 10px 30px rgba(0,0,0,0.3);}\n</style>\n</head>\n<body>\n<div class='card p-4' style='width:400px'>\n<div class='text-center mb-4'>\n<h2 class='text-primary fw-bold'>RadiNova AI</h2>\n<p class='text-muted'>Radiology Management System</p>\n</div>\n<form method='post'>\n{% csrf_token %}\n<div class='mb-3'><label class='form-label'>Username</label>\n<input type='text' name='username' class='form-control' required></div>\n<div class='mb-3'><label class='form-label'>Password</label>\n<input type='password' name='password' class='form-control' required></div>\n{% if error %}<div class='alert alert-danger'>{{ error }}</div>{% endif %}\n<button type='submit' class='btn btn-primary w-100'>Login</button>\n</form>\n</div>\n</body>\n</html>")
login_page.close()
print('Login page done!')
pe = open('templates/patient_edit.html','w',encoding='utf-8')
pe.write("{% extends 'base.html' %}\n{% block content %}\n<h2 class='mb-4'>Edit Patient</h2>\n<div class='card' style='max-width:600px'><div class='card-body'>\n<form method='post'>\n{% csrf_token %}\n<div class='mb-3'><label class='form-label'>Full Name</label>\n<input type='text' name='full_name' class='form-control' value='{{ patient.full_name }}' required></div>\n<div class='mb-3'><label class='form-label'>Date of Birth</label>\n<input type='date' name='date_of_birth' class='form-control' value='{{ patient.date_of_birth }}' required></div>\n<div class='mb-3'><label class='form-label'>Gender</label>\n<select name='gender' class='form-control'>\n<option {% if patient.gender == 'Male' %}selected{% endif %}>Male</option>\n<option {% if patient.gender == 'Female' %}selected{% endif %}>Female</option>\n<option {% if patient.gender == 'Other' %}selected{% endif %}>Other</option>\n</select></div>\n<div class='mb-3'><label class='form-label'>Contact Number</label>\n<input type='text' name='contact_number' class='form-control' value='{{ patient.contact_number }}' required></div>\n<div class='mb-3'><label class='form-label'>Medical History</label>\n<textarea name='medical_history' class='form-control' rows='3'>{{ patient.medical_history }}</textarea></div>\n<button type='submit' class='btn btn-primary'>Update</button>\n<a href='/patients/' class='btn btn-secondary'>Cancel</a>\n</form></div></div>\n{% endblock %}")
pe.close()
print('Patient edit template done!')
pl = open('templates/patients_list.html','w',encoding='utf-8')
pl.write("{% extends 'base.html' %}\n{% block content %}\n<div class='d-flex justify-content-between align-items-center mb-4'>\n<h2>Patients</h2>\n<a href='/patients/add/' class='btn btn-primary'>+ Add Patient</a>\n</div>\n<div class='card'><div class='card-body'>\n<table class='table table-hover'>\n<thead class='table-dark'>\n<tr><th>Name</th><th>Gender</th><th>Contact</th><th>Registered</th><th>Action</th></tr>\n</thead>\n<tbody>\n{% for patient in patients %}\n<tr>\n<td>{{ patient.full_name }}</td>\n<td>{{ patient.gender }}</td>\n<td>{{ patient.contact_number }}</td>\n<td>{{ patient.created_at|date:'d M Y' }}</td>\n<td>\n<a href='/patients/{{ patient.id }}/' class='btn btn-sm btn-info'>View</a>\n<a href='/patients/{{ patient.id }}/edit/' class='btn btn-sm btn-warning'>Edit</a>\n<a href='/patients/{{ patient.id }}/delete/' class='btn btn-sm btn-danger' onclick=\"return confirm('Delete karen?')\">Delete</a>\n</td>\n</tr>\n{% empty %}\n<tr><td colspan='5' class='text-center'>No patients found</td></tr>\n{% endfor %}\n</tbody>\n</table>\n</div></div>\n{% endblock %}")
pl.close()
print('Patients list updated!')
ae = open('templates/appointment_edit.html','w',encoding='utf-8')
ae.write("{% extends 'base.html' %}\n{% block content %}\n<h2 class='mb-4'>Edit Appointment</h2>\n<div class='card' style='max-width:600px'><div class='card-body'>\n<form method='post'>\n{% csrf_token %}\n<div class='mb-3'><label class='form-label'>Patient</label>\n<input type='text' class='form-control' value='{{ appt.patient.full_name }}' disabled></div>\n<div class='mb-3'><label class='form-label'>Scan Type</label>\n<select name='scan_type' class='form-control'>\n<option {% if appt.scan_type == 'X-Ray' %}selected{% endif %}>X-Ray</option>\n<option {% if appt.scan_type == 'Ultrasound' %}selected{% endif %}>Ultrasound</option>\n<option {% if appt.scan_type == 'MRI' %}selected{% endif %}>MRI</option>\n<option {% if appt.scan_type == 'CT Scan' %}selected{% endif %}>CT Scan</option>\n<option {% if appt.scan_type == 'Mammography' %}selected{% endif %}>Mammography</option>\n<option {% if appt.scan_type == 'Fluoroscopy' %}selected{% endif %}>Fluoroscopy</option>\n</select></div>\n<div class='mb-3'><label class='form-label'>Date and Time</label>\n<input type='datetime-local' name='appointment_date' class='form-control' required></div>\n<div class='mb-3'><label class='form-label'>Status</label>\n<select name='status' class='form-control'>\n<option {% if appt.status == 'Pending' %}selected{% endif %}>Pending</option>\n<option {% if appt.status == 'Completed' %}selected{% endif %}>Completed</option>\n<option {% if appt.status == 'Cancelled' %}selected{% endif %}>Cancelled</option>\n</select></div>\n<div class='mb-3'><label class='form-label'>Notes</label>\n<textarea name='notes' class='form-control' rows='3'>{{ appt.notes }}</textarea></div>\n<button type='submit' class='btn btn-primary'>Update</button>\n<a href='/appointments/' class='btn btn-secondary'>Cancel</a>\n</form></div></div>\n{% endblock %}")
ae.close()

al2 = open('templates/appointments_list.html','w',encoding='utf-8')
al2.write("{% extends 'base.html' %}\n{% block content %}\n<div class='d-flex justify-content-between align-items-center mb-4'>\n<h2>Appointments</h2>\n<a href='/appointments/add/' class='btn btn-primary'>+ New Appointment</a>\n</div>\n<div class='card'><div class='card-body'>\n<table class='table table-hover'>\n<thead class='table-dark'><tr><th>Patient</th><th>Scan Type</th><th>Date</th><th>Status</th><th>Action</th></tr></thead>\n<tbody>\n{% for appt in appointments %}\n<tr>\n<td>{{ appt.patient.full_name }}</td>\n<td>{{ appt.scan_type }}</td>\n<td>{{ appt.appointment_date|date:'d M Y H:i' }}</td>\n<td><span class='badge bg-warning'>{{ appt.status }}</span></td>\n<td>\n<a href='/appointments/{{ appt.id }}/' class='btn btn-sm btn-info'>View</a>\n<a href='/appointments/{{ appt.id }}/edit/' class='btn btn-sm btn-warning'>Edit</a>\n<a href='/appointments/{{ appt.id }}/delete/' class='btn btn-sm btn-danger' onclick=\"return confirm('Delete karen?')\">Delete</a>\n</td>\n</tr>\n{% empty %}\n<tr><td colspan='5' class='text-center'>No appointments</td></tr>\n{% endfor %}\n</tbody></table>\n</div></div>\n{% endblock %}")
al2.close()
print('Appointments updated!')
pl2 = open('templates/patients_list.html','w',encoding='utf-8')
pl2.write("{% extends 'base.html' %}\n{% block content %}\n<div class='d-flex justify-content-between align-items-center mb-4'>\n<h2>Patients</h2>\n<a href='/patients/add/' class='btn btn-primary'>+ Add Patient</a>\n</div>\n<form method='get' class='mb-3'>\n<div class='input-group'>\n<input type='text' name='q' value='{{ query }}' class='form-control' placeholder='Patient name search karo...'>\n<button type='submit' class='btn btn-outline-primary'>Search</button>\n<a href='/patients/' class='btn btn-outline-secondary'>Clear</a>\n</div>\n</form>\n<div class='card'><div class='card-body'>\n<table class='table table-hover'>\n<thead class='table-dark'>\n<tr><th>Name</th><th>Gender</th><th>Contact</th><th>Registered</th><th>Action</th></tr>\n</thead>\n<tbody>\n{% for patient in patients %}\n<tr>\n<td>{{ patient.full_name }}</td>\n<td>{{ patient.gender }}</td>\n<td>{{ patient.contact_number }}</td>\n<td>{{ patient.created_at|date:'d M Y' }}</td>\n<td>\n<a href='/patients/{{ patient.id }}/' class='btn btn-sm btn-info'>View</a>\n<a href='/patients/{{ patient.id }}/edit/' class='btn btn-sm btn-warning'>Edit</a>\n<a href='/patients/{{ patient.id }}/delete/' class='btn btn-sm btn-danger' onclick=\"return confirm('Delete karen?')\">Delete</a>\n</td>\n</tr>\n{% empty %}\n<tr><td colspan='5' class='text-center'>Koi patient nahi mila</td></tr>\n{% endfor %}\n</tbody>\n</table>\n</div></div>\n{% endblock %}")
pl2.close()
print('Search added!')
sl2 = open('templates/scans_list.html','w',encoding='utf-8')
sl2.write("{% extends 'base.html' %}\n{% block content %}\n<div class='d-flex justify-content-between align-items-center mb-4'>\n<h2>Scan Records</h2>\n<a href='/radiology/add/' class='btn btn-primary'>+ New Scan</a>\n</div>\n<div class='card'><div class='card-body'>\n<table class='table table-hover'>\n<thead class='table-dark'><tr><th>Patient</th><th>Scan Type</th><th>Date</th><th>Action</th></tr></thead>\n<tbody>\n{% for scan in scans %}\n<tr>\n<td>{{ scan.patient.full_name }}</td>\n<td>{{ scan.scan_category }}</td>\n<td>{{ scan.scan_date|date:'d M Y' }}</td>\n<td>\n<a href='/radiology/{{ scan.id }}/' class='btn btn-sm btn-info'>View</a>\n<a href='/radiology/{{ scan.id }}/delete/' class='btn btn-sm btn-danger' onclick=\"return confirm('Delete karen?')\">Delete</a>\n</td>\n</tr>\n{% empty %}\n<tr><td colspan='4' class='text-center'>No scans found</td></tr>\n{% endfor %}\n</tbody></table>\n</div></div>\n{% endblock %}")
sl2.close()
print('Scans updated!')
al3 = open('templates/appointments_list.html','w',encoding='utf-8')
al3.write("{% extends 'base.html' %}\n{% block content %}\n<div class='d-flex justify-content-between align-items-center mb-4'>\n<h2>Appointments</h2>\n<a href='/appointments/add/' class='btn btn-primary'>+ New Appointment</a>\n</div>\n<form method='get' class='mb-3'>\n<div class='input-group'>\n<input type='text' name='q' value='{{ query }}' class='form-control' placeholder='Patient name search karo...'>\n<button type='submit' class='btn btn-outline-primary'>Search</button>\n<a href='/appointments/' class='btn btn-outline-secondary'>Clear</a>\n</div>\n</form>\n<div class='card'><div class='card-body'>\n<table class='table table-hover'>\n<thead class='table-dark'><tr><th>Patient</th><th>Scan Type</th><th>Date</th><th>Status</th><th>Action</th></tr></thead>\n<tbody>\n{% for appt in appointments %}\n<tr>\n<td>{{ appt.patient.full_name }}</td>\n<td>{{ appt.scan_type }}</td>\n<td>{{ appt.appointment_date|date:'d M Y H:i' }}</td>\n<td><span class='badge bg-warning'>{{ appt.status }}</span></td>\n<td>\n<a href='/appointments/{{ appt.id }}/' class='btn btn-sm btn-info'>View</a>\n<a href='/appointments/{{ appt.id }}/edit/' class='btn btn-sm btn-warning'>Edit</a>\n<a href='/appointments/{{ appt.id }}/delete/' class='btn btn-sm btn-danger' onclick=\"return confirm('Delete karen?')\">Delete</a>\n</td>\n</tr>\n{% empty %}\n<tr><td colspan='5' class='text-center'>Koi appointment nahi mili</td></tr>\n{% endfor %}\n</tbody></table>\n</div></div>\n{% endblock %}")
al3.close()
print('Appointments search done!')
base = open('templates/base.html','w',encoding='utf-8')
base.write("""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>RadiNova AI</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: 'Segoe UI', sans-serif; background: #f0f2f5; }
.sidebar {
  width: 250px; height: 100vh; position: fixed; left: 0; top: 0;
  background: linear-gradient(180deg, #0f172a 0%, #1e3a5f 100%);
  padding: 0; z-index: 100; box-shadow: 4px 0 15px rgba(0,0,0,0.3);
}
.sidebar-brand {
  padding: 25px 20px;
  border-bottom: 1px solid rgba(255,255,255,0.1);
  text-align: center;
}
.sidebar-brand h4 {
  color: #38bdf8; font-weight: 700; font-size: 1.4rem; margin: 0;
  letter-spacing: 1px;
}
.sidebar-brand small { color: rgba(255,255,255,0.5); font-size: 0.7rem; }
.sidebar-menu { padding: 15px 0; }
.sidebar-menu a {
  display: flex; align-items: center; gap: 12px;
  padding: 12px 25px; color: rgba(255,255,255,0.7);
  text-decoration: none; font-size: 0.9rem; font-weight: 500;
  transition: all 0.3s; border-left: 3px solid transparent;
}
.sidebar-menu a:hover, .sidebar-menu a.active {
  color: #fff; background: rgba(56,189,248,0.15);
  border-left: 3px solid #38bdf8;
}
.sidebar-menu a i { width: 20px; text-align: center; font-size: 1rem; }
.sidebar-menu .menu-label {
  padding: 15px 25px 5px; color: rgba(255,255,255,0.3);
  font-size: 0.7rem; text-transform: uppercase; letter-spacing: 2px;
}
.sidebar-footer {
  position: absolute; bottom: 0; width: 100%;
  padding: 15px 20px; border-top: 1px solid rgba(255,255,255,0.1);
}
.sidebar-footer a {
  display: flex; align-items: center; gap: 10px;
  color: rgba(255,255,255,0.6); text-decoration: none; font-size: 0.85rem;
  transition: color 0.3s;
}
.sidebar-footer a:hover { color: #f87171; }
.main-content {
  margin-left: 250px; min-height: 100vh;
}
.top-bar {
  background: #fff; padding: 15px 30px;
  display: flex; justify-content: space-between; align-items: center;
  box-shadow: 0 2px 10px rgba(0,0,0,0.08); position: sticky; top: 0; z-index: 99;
}
.top-bar .page-title { font-weight: 600; color: #1e3a5f; font-size: 1.1rem; }
.top-bar .user-info {
  display: flex; align-items: center; gap: 10px;
  color: #64748b; font-size: 0.9rem;
}
.top-bar .user-avatar {
  width: 35px; height: 35px; border-radius: 50%;
  background: linear-gradient(135deg, #38bdf8, #1e3a5f);
  display: flex; align-items: center; justify-content: center;
  color: #fff; font-weight: 700; font-size: 0.9rem;
}
.content-area { padding: 30px; }
.card {
  border: none; border-radius: 12px;
  box-shadow: 0 2px 15px rgba(0,0,0,0.08); margin-bottom: 20px;
}
.card-header {
  background: #fff; border-bottom: 1px solid #f1f5f9;
  border-radius: 12px 12px 0 0 !important;
  padding: 15px 20px; font-weight: 600; color: #1e3a5f;
}
.btn-primary { background: #2563eb; border-color: #2563eb; border-radius: 8px; }
.btn-primary:hover { background: #1d4ed8; border-color: #1d4ed8; }
.btn-danger { border-radius: 8px; }
.btn-warning { border-radius: 8px; }
.btn-info { border-radius: 8px; }
.table thead th { font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px; }
.form-control, .form-select { border-radius: 8px; border: 1px solid #e2e8f0; }
.form-control:focus { border-color: #38bdf8; box-shadow: 0 0 0 3px rgba(56,189,248,0.15); }
.badge { border-radius: 6px; padding: 5px 10px; }
h2 { color: #1e3a5f; font-weight: 700; }
</style>
</head>
<body>
<div class="sidebar">
  <div class="sidebar-brand">
    <h4><i class="fas fa-radiation"></i> RadiNova AI</h4>
    <small>Radiology Management</small>
  </div>
  <div class="sidebar-menu">
    <div class="menu-label">Main Menu</div>
    <a href="/dashboard/"><i class="fas fa-chart-pie"></i> Dashboard</a>
    <a href="/patients/"><i class="fas fa-user-injured"></i> Patients</a>
    <a href="/appointments/"><i class="fas fa-calendar-check"></i> Appointments</a>
    <div class="menu-label">Radiology</div>
    <a href="/radiology/"><i class="fas fa-x-ray"></i> Scans</a>
    <a href="/reports/"><i class="fas fa-file-medical"></i> Reports</a>
  </div>
  <div class="sidebar-footer">
    <a href="/logout/"><i class="fas fa-sign-out-alt"></i> Logout</a>
  </div>
</div>
<div class="main-content">
  <div class="top-bar">
    <span class="page-title">Welcome to RadiNova AI</span>
    <div class="user-info">
      <div class="user-avatar">D</div>
      <span>Danish</span>
    </div>
  </div>
  <div class="content-area">
    {% block content %}{% endblock %}
  </div>
</div>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>""")
base.close()
print('Base template upgraded!')
dash = open('templates/dashboard.html','w',encoding='utf-8')
dash.write("""{% extends 'base.html' %}
{% block content %}
<div class="row g-4 mb-4">
  <div class="col-md-3">
    <div class="card" style="border-left: 4px solid #2563eb;">
      <div class="card-body d-flex justify-content-between align-items-center">
        <div>
          <p class="text-muted mb-1" style="font-size:0.8rem;text-transform:uppercase;">Total Patients</p>
          <h3 class="fw-bold text-primary mb-0">{{ total_patients }}</h3>
        </div>
        <div style="width:50px;height:50px;background:#eff6ff;border-radius:12px;display:flex;align-items:center;justify-content:center;">
          <i class="fas fa-user-injured text-primary fa-lg"></i>
        </div>
      </div>
    </div>
  </div>
  <div class="col-md-3">
    <div class="card" style="border-left: 4px solid #16a34a;">
      <div class="card-body d-flex justify-content-between align-items-center">
        <div>
          <p class="text-muted mb-1" style="font-size:0.8rem;text-transform:uppercase;">Appointments</p>
          <h3 class="fw-bold text-success mb-0">{{ total_appointments }}</h3>
        </div>
        <div style="width:50px;height:50px;background:#f0fdf4;border-radius:12px;display:flex;align-items:center;justify-content:center;">
          <i class="fas fa-calendar-check text-success fa-lg"></i>
        </div>
      </div>
    </div>
  </div>
  <div class="col-md-3">
    <div class="card" style="border-left: 4px solid #d97706;">
      <div class="card-body d-flex justify-content-between align-items-center">
        <div>
          <p class="text-muted mb-1" style="font-size:0.8rem;text-transform:uppercase;">Total Scans</p>
          <h3 class="fw-bold text-warning mb-0">{{ total_scans }}</h3>
        </div>
        <div style="width:50px;height:50px;background:#fffbeb;border-radius:12px;display:flex;align-items:center;justify-content:center;">
          <i class="fas fa-x-ray text-warning fa-lg"></i>
        </div>
      </div>
    </div>
  </div>
  <div class="col-md-3">
    <div class="card" style="border-left: 4px solid #dc2626;">
      <div class="card-body d-flex justify-content-between align-items-center">
        <div>
          <p class="text-muted mb-1" style="font-size:0.8rem;text-transform:uppercase;">Reports</p>
          <h3 class="fw-bold text-danger mb-0">{{ total_reports }}</h3>
        </div>
        <div style="width:50px;height:50px;background:#fef2f2;border-radius:12px;display:flex;align-items:center;justify-content:center;">
          <i class="fas fa-file-medical text-danger fa-lg"></i>
        </div>
      </div>
    </div>
  </div>
</div>

<div class="row g-4">
  <div class="col-md-7">
    <div class="card">
      <div class="card-header d-flex justify-content-between align-items-center">
        <span><i class="fas fa-chart-bar me-2 text-primary"></i>Scan Types Overview</span>
      </div>
      <div class="card-body">
        <canvas id="scanChart" height="250"></canvas>
      </div>
    </div>
  </div>
  <div class="col-md-5">
    <div class="card">
      <div class="card-header">
        <span><i class="fas fa-chart-pie me-2 text-primary"></i>Appointment Status</span>
      </div>
      <div class="card-body">
        <canvas id="statusChart" height="250"></canvas>
      </div>
    </div>
  </div>
</div>

<div class="row g-4 mt-1">
  <div class="col-md-12">
    <div class="card">
      <div class="card-header">
        <span><i class="fas fa-clock me-2 text-primary"></i>Recent Patients</span>
      </div>
      <div class="card-body p-0">
        <table class="table table-hover mb-0">
          <thead class="table-light">
            <tr><th>Name</th><th>Gender</th><th>Contact</th><th>Registered</th></tr>
          </thead>
          <tbody>
            {% for p in recent_patients %}
            <tr>
              <td><i class="fas fa-user-circle text-primary me-2"></i>{{ p.full_name }}</td>
              <td>{{ p.gender }}</td>
              <td>{{ p.contact_number }}</td>
              <td>{{ p.created_at|date:'d M Y' }}</td>
            </tr>
            {% empty %}
            <tr><td colspan="4" class="text-center text-muted py-3">Koi patient nahi hai</td></tr>
            {% endfor %}
          </tbody>
        </table>
      </div>
    </div>
  </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
const scanCtx = document.getElementById('scanChart').getContext('2d');
new Chart(scanCtx, {
  type: 'bar',
  data: {
    labels: ['X-Ray', 'MRI', 'CT Scan', 'Ultrasound', 'Mammography', 'Fluoroscopy'],
    datasets: [{
      label: 'Scans',
      data: {{ scan_counts|safe }},
      backgroundColor: ['#3b82f6','#8b5cf6','#f59e0b','#10b981','#ef4444','#06b6d4'],
      borderRadius: 8,
    }]
  },
  options: { responsive: true, plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true, ticks: { stepSize: 1 } } } }
});

const statusCtx = document.getElementById('statusChart').getContext('2d');
new Chart(statusCtx, {
  type: 'doughnut',
  data: {
    labels: ['Pending', 'Completed', 'Cancelled'],
    datasets: [{
      data: {{ status_counts|safe }},
      backgroundColor: ['#f59e0b','#10b981','#ef4444'],
      borderWidth: 0,
    }]
  },
  options: { responsive: true, plugins: { legend: { position: 'bottom' } }, cutout: '65%' }
});
</script>
{% endblock %}""")
dash.close()
print('Dashboard upgraded!')
ra2 = open('templates/reports_add.html','w',encoding='utf-8')
ra2.write("""{% extends 'base.html' %}
{% block content %}
<h2 class='mb-4'>Create Report</h2>
<div class='row'>
<div class='col-md-8'>
<div class='card'>
<div class='card-header'><i class='fas fa-file-medical me-2 text-primary'></i>Report Details</div>
<div class='card-body'>
<p><strong>Patient:</strong> {{ scan.patient.full_name }}</p>
<p><strong>Scan Type:</strong> {{ scan.scan_category }}</p>
<form method='post'>
{% csrf_token %}
<div class='mb-3'>
<label class='form-label fw-bold'>Report Text</label>
<textarea name='report_text' id='report_text' class='form-control' rows='6' required>{% if ai_suggestion %}{{ ai_suggestion }}{% endif %}</textarea>
</div>
<button type='submit' class='btn btn-success'><i class='fas fa-save me-2'></i>Save Report</button>
<a href='/radiology/' class='btn btn-secondary ms-2'>Cancel</a>
</form>
</div>
</div>
</div>
<div class='col-md-4'>
{% if ai_suggestion %}
<div class='card border-0' style='background:linear-gradient(135deg,#eff6ff,#dbeafe);'>
<div class='card-body'>
<h6 class='fw-bold text-primary mb-3'><i class='fas fa-robot me-2'></i>AI Suggestion</h6>
<p class='text-muted' style='font-size:0.85rem;'>AI ne yeh findings suggest ki hain — aap edit kar sakte hain.</p>
<hr>
<p style='font-size:0.9rem;'>{{ ai_suggestion }}</p>
<button onclick="document.getElementById('report_text').value='{{ ai_suggestion|escapejs }}'" class='btn btn-primary btn-sm w-100 mt-2'>
<i class='fas fa-magic me-2'></i>AI Text Use Karo
</button>
</div>
</div>
{% else %}
<div class='card border-0' style='background:#f8fafc;'>
<div class='card-body text-center text-muted'>
<i class='fas fa-robot fa-3x mb-3 text-primary opacity-50'></i>
<p style='font-size:0.85rem;'>AI suggestion load ho rahi hai...</p>
</div>
</div>
{% endif %}
</div>
</div>
{% endblock %}""")
ra2.close()
print('AI report template done!')
# Appointments add template with fees
aa2 = open('templates/appointments_add.html','w',encoding='utf-8')
aa2.write("""{% extends 'base.html' %}
{% block content %}
<h2 class='mb-4'>New Appointment</h2>
<div class='card' style='max-width:650px'>
<div class='card-body'>
<form method='post'>
{% csrf_token %}
<div class='mb-3'>
<label class='form-label fw-bold'>Patient</label>
<select name='patient_id' class='form-control' required>
<option value=''>-- Patient Select Karo --</option>
{% for p in patients %}<option value='{{ p.id }}'>{{ p.full_name }}</option>{% endfor %}
</select>
</div>
<div class='mb-3'>
<label class='form-label fw-bold'>Scan Type</label>
<select name='scan_type' class='form-control' required onchange='updateFee(this.value)'>
<option value=''>-- Scan Type Select Karo --</option>
<option value='X-Ray'>X-Ray — Rs. 500</option>
<option value='Ultrasound'>Ultrasound — Rs. 1,500</option>
<option value='MRI'>MRI — Rs. 8,000</option>
<option value='CT Scan'>CT Scan — Rs. 5,000</option>
<option value='Mammography'>Mammography — Rs. 3,000</option>
<option value='Fluoroscopy'>Fluoroscopy — Rs. 4,000</option>
</select>
</div>
<div class='mb-3'>
<label class='form-label fw-bold'>Fees</label>
<div class='input-group'>
<span class='input-group-text'>Rs.</span>
<input type='text' id='fees_display' class='form-control' readonly placeholder='Scan type select karne par fees aayegi'>
</div>
</div>
<div class='mb-3'>
<label class='form-label fw-bold'>Payment Status</label>
<select name='payment_status' class='form-control' required>
<option value='Paid'>✅ Paid</option>
<option value='Unpaid'>❌ Unpaid</option>
</select>
</div>
<div class='mb-3'>
<label class='form-label fw-bold'>Date and Time</label>
<input type='datetime-local' name='appointment_date' class='form-control' required>
</div>
<div class='mb-3'>
<label class='form-label fw-bold'>Notes</label>
<textarea name='notes' class='form-control' rows='3'></textarea>
</div>
<button type='submit' class='btn btn-primary'>Save Appointment</button>
<a href='/appointments/' class='btn btn-secondary ms-2'>Cancel</a>
</form>
</div></div>
<script>
const fees = {'X-Ray':500,'Ultrasound':1500,'MRI':8000,'CT Scan':5000,'Mammography':3000,'Fluoroscopy':4000};
function updateFee(scan){
  document.getElementById('fees_display').value = fees[scan] ? fees[scan].toLocaleString() : '';
}
</script>
{% endblock %}""")
aa2.close()

# Appointments list with payment filter
al4 = open('templates/appointments_list.html','w',encoding='utf-8')
al4.write("""{% extends 'base.html' %}
{% block content %}
<div class='d-flex justify-content-between align-items-center mb-4'>
<h2>Appointments</h2>
<a href='/appointments/add/' class='btn btn-primary'>+ New Appointment</a>
</div>
<form method='get' class='mb-3'>
<div class='row g-2'>
<div class='col-md-6'>
<div class='input-group'>
<input type='text' name='q' value='{{ query }}' class='form-control' placeholder='Patient name search karo...'>
<button type='submit' class='btn btn-outline-primary'>Search</button>
<a href='/appointments/' class='btn btn-outline-secondary'>Clear</a>
</div>
</div>
<div class='col-md-4'>
<select name='payment' class='form-control' onchange='this.form.submit()'>
<option value=''>-- Sab Appointments --</option>
<option value='Paid' {% if payment_filter == 'Paid' %}selected{% endif %}>✅ Paid Only</option>
<option value='Unpaid' {% if payment_filter == 'Unpaid' %}selected{% endif %}>❌ Unpaid Only</option>
</select>
</div>
</div>
</form>
<div class='card'><div class='card-body'>
<table class='table table-hover'>
<thead class='table-dark'><tr><th>Patient</th><th>Scan Type</th><th>Fees</th><th>Payment</th><th>Date</th><th>Status</th><th>Action</th></tr></thead>
<tbody>
{% for appt in appointments %}
<tr>
<td>{{ appt.patient.full_name }}</td>
<td>{{ appt.scan_type }}</td>
<td>Rs. {{ appt.fees|default:0 }}</td>
<td>
{% if appt.payment_status == 'Paid' %}
<span class='badge bg-success'>✅ Paid</span>
{% else %}
<span class='badge bg-danger'>❌ Unpaid</span>
{% endif %}
</td>
<td>{{ appt.appointment_date|date:'d M Y H:i' }}</td>
<td><span class='badge bg-warning'>{{ appt.status }}</span></td>
<td>
<a href='/appointments/{{ appt.id }}/' class='btn btn-sm btn-info'>View</a>
<a href='/appointments/{{ appt.id }}/edit/' class='btn btn-sm btn-warning'>Edit</a>
<a href='/appointments/{{ appt.id }}/delete/' class='btn btn-sm btn-danger' onclick="return confirm('Delete karen?')">Delete</a>
</td>
</tr>
{% empty %}
<tr><td colspan='7' class='text-center text-muted py-3'>Koi appointment nahi mili</td></tr>
{% endfor %}
</tbody></table>
</div></div>
{% endblock %}""")
al4.close()
print('Fees feature done!')
al5 = open('templates/appointments_list.html','w',encoding='utf-8')
al5.write("""{% extends 'base.html' %}
{% block content %}
<div class='d-flex justify-content-between align-items-center mb-4'>
<h2>Appointments</h2>
<a href='/appointments/add/' class='btn btn-primary'>+ New Appointment</a>
</div>
<div class='row g-3 mb-4'>
<div class='col-md-2'><div class='card text-center' style='border-left:4px solid #10b981'><div class='card-body py-2'><div class='fw-bold text-success fs-4'>{{ total_paid }}</div><small class='text-muted'>Paid</small></div></div></div>
<div class='col-md-2'><div class='card text-center' style='border-left:4px solid #ef4444'><div class='card-body py-2'><div class='fw-bold text-danger fs-4'>{{ total_unpaid }}</div><small class='text-muted'>Unpaid</small></div></div></div>
<div class='col-md-2'><div class='card text-center' style='border-left:4px solid #f59e0b'><div class='card-body py-2'><div class='fw-bold text-warning fs-4'>{{ total_pending }}</div><small class='text-muted'>Pending</small></div></div></div>
<div class='col-md-2'><div class='card text-center' style='border-left:4px solid #2563eb'><div class='card-body py-2'><div class='fw-bold text-primary fs-4'>{{ total_completed }}</div><small class='text-muted'>Completed</small></div></div></div>
<div class='col-md-2'><div class='card text-center' style='border-left:4px solid #6b7280'><div class='card-body py-2'><div class='fw-bold text-secondary fs-4'>{{ total_cancelled }}</div><small class='text-muted'>Cancelled</small></div></div></div>
</div>
<form method='get' class='mb-3'>
<div class='row g-2'>
<div class='col-md-4'><div class='input-group'><input type='text' name='q' value='{{ query }}' class='form-control' placeholder='Patient name search karo...'><button type='submit' class='btn btn-outline-primary'>Search</button><a href='/appointments/' class='btn btn-outline-secondary'>Clear</a></div></div>
<div class='col-md-3'><select name='payment' class='form-control' onchange='this.form.submit()'><option value=''>-- Payment Filter --</option><option value='Paid' {% if payment_filter == 'Paid' %}selected{% endif %}>✅ Paid Only</option><option value='Unpaid' {% if payment_filter == 'Unpaid' %}selected{% endif %}>❌ Unpaid Only</option></select></div>
<div class='col-md-3'><select name='status' class='form-control' onchange='this.form.submit()'><option value=''>-- Status Filter --</option><option value='Pending' {% if status_filter == 'Pending' %}selected{% endif %}>⏳ Pending</option><option value='Completed' {% if status_filter == 'Completed' %}selected{% endif %}>✅ Completed</option><option value='Cancelled' {% if status_filter == 'Cancelled' %}selected{% endif %}>❌ Cancelled</option></select></div>
</div>
</form>
<div class='card'><div class='card-body p-0'>
<table class='table table-hover mb-0'>
<thead class='table-dark'><tr><th>Patient</th><th>Scan Type</th><th>Fees</th><th>Payment</th><th>Date</th><th>Status</th><th>Action</th></tr></thead>
<tbody>
{% for appt in appointments %}
<tr>
<td><strong>{{ appt.patient.full_name }}</strong></td>
<td>{{ appt.scan_type }}</td>
<td>Rs. {{ appt.fees|default:0 }}</td>
<td>{% if appt.payment_status == 'Paid' %}<span class='badge bg-success'>✅ Paid</span>{% else %}<span class='badge bg-danger'>❌ Unpaid</span>{% endif %}</td>
<td>{{ appt.appointment_date|date:'d M Y H:i' }}</td>
<td>{% if appt.status == 'Completed' %}<span class='badge bg-primary'>✅ Completed</span>{% elif appt.status == 'Cancelled' %}<span class='badge bg-secondary'>❌ Cancelled</span>{% else %}<span class='badge bg-warning'>⏳ Pending</span>{% endif %}</td>
<td>
<div class='d-flex gap-1 flex-wrap'>
{% if appt.payment_status == 'Paid' and appt.status == 'Pending' %}<a href='/appointments/{{ appt.id }}/complete/' class='btn btn-sm btn-success'>✅ Done</a>{% endif %}
{% if appt.payment_status == 'Unpaid' and appt.status == 'Pending' %}<a href='/appointments/{{ appt.id }}/cancel/' class='btn btn-sm btn-danger' onclick="return confirm('Cancel karen?')">❌ Cancel</a>{% endif %}
{% if appt.status == 'Cancelled' or appt.status == 'Completed' %}<a href='/appointments/{{ appt.id }}/pending/' class='btn btn-sm btn-warning'>⏳ Pending</a>{% endif %}
<a href='/appointments/{{ appt.id }}/edit/' class='btn btn-sm btn-info'>Edit</a>
<a href='/appointments/{{ appt.id }}/delete/' class='btn btn-sm btn-danger' onclick="return confirm('Delete karen?')">Del</a>
</div>
</td>
</tr>
{% empty %}
<tr><td colspan='7' class='text-center text-muted py-3'>Koi appointment nahi mili</td></tr>
{% endfor %}
</tbody></table>
</div></div>
{% endblock %}""")
al5.close()
print('Smart appointments done!')
pe = open('templates/patient_edit.html','w',encoding='utf-8')
pe.write("{% extends 'base.html' %}\n{% block content %}\n<h2 class='mb-4'>Edit Patient</h2>\n<div class='card' style='max-width:600px'><div class='card-body'>\n<form method='post'>\n{% csrf_token %}\n<div class='mb-3'><label class='form-label'>Full Name</label><input type='text' name='full_name' class='form-control' value='{{ patient.full_name }}' required></div>\n<div class='mb-3'><label class='form-label'>Date of Birth</label><input type='date' name='date_of_birth' class='form-control' value='{{ patient.date_of_birth }}' required></div>\n<div class='mb-3'><label class='form-label'>Gender</label><select name='gender' class='form-control'>\n<option {% if patient.gender == 'Male' %}selected{% endif %}>Male</option>\n<option {% if patient.gender == 'Female' %}selected{% endif %}>Female</option>\n<option {% if patient.gender == 'Other' %}selected{% endif %}>Other</option>\n</select></div>\n<div class='mb-3'><label class='form-label'>Contact Number</label><input type='text' name='contact_number' class='form-control' value='{{ patient.contact_number }}' required></div>\n<div class='mb-3'><label class='form-label'>Medical History</label><textarea name='medical_history' class='form-control' rows='3'>{{ patient.medical_history }}</textarea></div>\n<button type='submit' class='btn btn-primary'>Update</button>\n<a href='/patients/{{ patient.id }}/' class='btn btn-secondary'>Cancel</a>\n</form></div></div>\n{% endblock %}")
pe.close()
print('Patient edit done!')
pe2 = open('templates/patient_edit.html','w',encoding='utf-8')
pe2.write("{% extends 'base.html' %}\n{% block content %}\n<h2 class='mb-4'>Edit Patient</h2>\n<div class='card' style='max-width:600px'><div class='card-body'>\n<form method='post'>\n{% csrf_token %}\n<div class='mb-3'><label class='form-label'>Full Name</label><input type='text' name='full_name' class='form-control' value='{{ patient.full_name }}' required></div>\n<div class='mb-3'><label class='form-label'>Date of Birth</label><input type='date' name='date_of_birth' class='form-control' value='{{ patient.date_of_birth|date:\"Y-m-d\" }}' required></div>\n<div class='mb-3'><label class='form-label'>Gender</label><select name='gender' class='form-control'>\n<option {% if patient.gender == 'Male' %}selected{% endif %}>Male</option>\n<option {% if patient.gender == 'Female' %}selected{% endif %}>Female</option>\n<option {% if patient.gender == 'Other' %}selected{% endif %}>Other</option>\n</select></div>\n<div class='mb-3'><label class='form-label'>Contact Number</label><input type='text' name='contact_number' class='form-control' value='{{ patient.contact_number }}' required></div>\n<div class='mb-3'><label class='form-label'>Medical History</label><textarea name='medical_history' class='form-control' rows='3'>{{ patient.medical_history }}</textarea></div>\n<button type='submit' class='btn btn-warning'>Update Patient</button>\n<a href='/patients/{{ patient.id }}/' class='btn btn-secondary'>Cancel</a>\n</form></div></div>\n{% endblock %}")
pe2.close()
print('Patient edit fixed!')
pd = open('templates/patient_delete.html','w',encoding='utf-8')
pd.write("{% extends 'base.html' %}\n{% block content %}\n<h2 class='mb-4'>Delete Patient</h2>\n<div class='card' style='max-width:500px'><div class='card-body'>\n<p>Are you sure you want to delete <strong>{{ patient.full_name }}</strong>?</p>\n<form method='post'>\n{% csrf_token %}\n<button type='submit' class='btn btn-danger'>Yes, Delete</button>\n<a href='/patients/' class='btn btn-secondary'>Cancel</a>\n</form>\n</div></div>\n{% endblock %}")
pd.close()
print('Patient delete done!')
open('appointments/urls.py','w',encoding='utf-8').write(
"from django.urls import path\nfrom . import views\n\nurlpatterns = [\n    path('', views.appointments_list, name='appointments_list'),\n    path('add/', views.appointments_add, name='appointments_add'),\n    path('<int:pk>/', views.appointment_detail, name='appointment_detail'),\n    path('<int:pk>/edit/', views.appointment_edit, name='appointment_edit'),\n    path('<int:pk>/delete/', views.appointment_delete, name='appointment_delete'),\n    path('<int:pk>/complete/', views.appointment_complete, name='appointment_complete'),\n    path('<int:pk>/cancel/', views.appointment_cancel, name='appointment_cancel'),\n]\n"
)
print('Appointments urls fixed!')
open('appointments/urls.py','w',encoding='utf-8').write(
"from django.urls import path\nfrom . import views\n\nurlpatterns = [\n    path('', views.appointments_list, name='appointments_list'),\n    path('add/', views.appointments_add, name='appointments_add'),\n    path('<int:pk>/', views.appointment_detail, name='appointment_detail'),\n    path('<int:pk>/edit/', views.appointment_edit, name='appointment_edit'),\n    path('<int:pk>/delete/', views.appointment_delete, name='appointment_delete'),\n    path('<int:pk>/complete/', views.appointment_complete, name='appointment_complete'),\n    path('<int:pk>/cancel/', views.appointment_cancel, name='appointment_cancel'),\n    path('<int:pk>/pending/', views.appointment_pending, name='appointment_pending'),\n]\n"
)
print('Appointments urls v2 fixed!')
apd = open('templates/appointment_delete.html','w',encoding='utf-8')
apd.write("{% extends 'base.html' %}\n{% block content %}\n<h2 class='mb-4'>Delete Appointment</h2>\n<div class='card' style='max-width:500px'><div class='card-body'>\n<p>Are you sure you want to delete appointment of <strong>{{ appt.patient.full_name }}</strong>?</p>\n<p>Scan: {{ appt.scan_type }} | Date: {{ appt.appointment_date|date:'d M Y' }}</p>\n<form method='post'>\n{% csrf_token %}\n<button type='submit' class='btn btn-danger'>Yes, Delete</button>\n<a href='/appointments/' class='btn btn-secondary'>Cancel</a>\n</form>\n</div></div>\n{% endblock %}")
apd.close()
print('Appointment delete template done!')
open('radiology/urls.py','w',encoding='utf-8').write(
"from django.urls import path\nfrom . import views\n\nurlpatterns = [\n    path('', views.scans_list, name='scans_list'),\n    path('add/', views.scans_add, name='scans_add'),\n    path('<int:pk>/', views.scan_detail, name='scan_detail'),\n    path('<int:pk>/delete/', views.scan_delete, name='scan_delete'),\n]\n"
)

sdd = open('templates/scan_delete.html','w',encoding='utf-8')
sdd.write("{% extends 'base.html' %}\n{% block content %}\n<h2 class='mb-4'>Delete Scan</h2>\n<div class='card' style='max-width:500px'><div class='card-body'>\n<p>Are you sure you want to delete scan of <strong>{{ scan.patient.full_name }}</strong>?</p>\n<p>Type: {{ scan.scan_category }} | Date: {{ scan.scan_date|date:'d M Y' }}</p>\n<form method='post'>\n{% csrf_token %}\n<button type='submit' class='btn btn-danger'>Yes, Delete</button>\n<a href='/radiology/' class='btn btn-secondary'>Cancel</a>\n</form>\n</div></div>\n{% endblock %}")
sdd.close()
print('Scan delete done!')
al2 = open('templates/appointments_list.html','w',encoding='utf-8')
al2.write("{% extends 'base.html' %}\n{% block content %}\n<div class='d-flex justify-content-between align-items-center mb-4'>\n<h2>Appointments</h2>\n<a href='/appointments/add/' class='btn btn-primary'>+ New Appointment</a>\n</div>\n\n<div class='row mb-3'>\n<div class='col'><a href='?payment=Paid' class='btn btn-success w-100'>Paid ({{ paid }})</a></div>\n<div class='col'><a href='?payment=Unpaid' class='btn btn-danger w-100'>Unpaid ({{ unpaid }})</a></div>\n<div class='col'><a href='?status=Pending' class='btn btn-warning w-100'>Pending ({{ pending }})</a></div>\n<div class='col'><a href='?status=Completed' class='btn btn-info w-100'>Completed ({{ completed }})</a></div>\n<div class='col'><a href='?status=Cancelled' class='btn btn-secondary w-100'>Cancelled ({{ cancelled }})</a></div>\n<div class='col'><a href='/appointments/' class='btn btn-dark w-100'>Show All</a></div>\n</div>\n\n<div class='card mb-3'><div class='card-body'>\n<form method='get' class='row g-2'>\n<div class='col-md-6'><input type='text' name='q' class='form-control' placeholder='Patient name search...' value='{{ request.GET.q }}'></div>\n<div class='col-md-2'><button type='submit' class='btn btn-primary w-100'>Search</button></div>\n<div class='col-md-2'><a href='/appointments/' class='btn btn-secondary w-100'>Clear</a></div>\n</form>\n</div></div>\n\n<div class='card'><div class='card-body'>\n<table class='table table-hover'>\n<thead class='table-dark'><tr><th>Patient</th><th>Scan Type</th><th>Fees</th><th>Payment</th><th>Date</th><th>Status</th><th>Action</th></tr></thead>\n<tbody>\n{% for appt in appointments %}\n<tr>\n<td><strong>{{ appt.patient.full_name }}</strong></td>\n<td>{{ appt.scan_type }}</td>\n<td>Rs. {{ appt.fees }}</td>\n<td>{% if appt.payment_status == 'Paid' %}<span class='badge bg-success'>Paid</span>{% else %}<span class='badge bg-danger'>Unpaid</span>{% endif %}</td>\n<td>{{ appt.appointment_date|date:'d M Y H:i' }}</td>\n<td>{% if appt.status == 'Completed' %}<span class='badge bg-info'>Completed</span>{% elif appt.status == 'Cancelled' %}<span class='badge bg-secondary'>Cancelled</span>{% else %}<span class='badge bg-warning'>Pending</span>{% endif %}</td>\n<td>\n<a href='/appointments/{{ appt.id }}/' class='btn btn-sm btn-primary'>View</a>\n<a href='/appointments/{{ appt.id }}/edit/' class='btn btn-sm btn-warning'>Edit</a>\n<a href='/appointments/{{ appt.id }}/delete/' class='btn btn-sm btn-danger'>Del</a>\n</td>\n</tr>\n{% empty %}\n<tr><td colspan='7' class='text-center'>No appointments found</td></tr>\n{% endfor %}\n</tbody></table>\n</div></div>\n{% endblock %}")
al2.close()
print('Appointments list updated!')
apd2 = open('templates/appointment_detail.html','w',encoding='utf-8')
apd2.write("{% extends 'base.html' %}\n{% block content %}\n<h2 class='mb-4'>Appointment Detail</h2>\n<div class='row'>\n<div class='col-md-6'>\n<div class='card mb-3'><div class='card-body'>\n<h5>Appointment Info</h5>\n<p><strong>Patient:</strong> {{ appt.patient.full_name }}</p>\n<p><strong>Scan Type:</strong> {{ appt.scan_type }}</p>\n<p><strong>Date:</strong> {{ appt.appointment_date|date:'d M Y H:i' }}</p>\n<p><strong>Notes:</strong> {{ appt.notes }}</p>\n<p><strong>Fees:</strong> Rs. {{ appt.fees }}</p>\n<p><strong>Payment:</strong> {% if appt.payment_status == 'Paid' %}<span class='badge bg-success fs-6'>Paid</span>{% else %}<span class='badge bg-danger fs-6'>Unpaid</span>{% endif %}</p>\n<p><strong>Status:</strong> {% if appt.status == 'Completed' %}<span class='badge bg-info fs-6'>Completed</span>{% elif appt.status == 'Cancelled' %}<span class='badge bg-secondary fs-6'>Cancelled</span>{% else %}<span class='badge bg-warning fs-6'>Pending</span>{% endif %}</p>\n</div></div>\n</div>\n<div class='col-md-6'>\n<div class='card mb-3'><div class='card-body'>\n<h5>Set Fees</h5>\n<form method='post'>\n{% csrf_token %}\n<input type='hidden' name='action' value='set_fees'>\n<div class='input-group'>\n<span class='input-group-text'>Rs.</span>\n<input type='number' name='fees' class='form-control' value='{{ appt.fees }}' min='0'>\n<button type='submit' class='btn btn-primary'>Save Fees</button>\n</div>\n</form>\n</div></div>\n<div class='card mb-3'><div class='card-body'>\n<h5>Payment Status</h5>\n<form method='post' class='d-flex gap-2'>\n{% csrf_token %}\n<button name='action' value='mark_paid' class='btn btn-success w-50'>Mark as Paid</button>\n<button name='action' value='mark_unpaid' class='btn btn-danger w-50'>Mark as Unpaid</button>\n</form>\n</div></div>\n<div class='card'><div class='card-body'>\n<h5>Appointment Status</h5>\n<form method='post' class='d-flex gap-2 flex-wrap'>\n{% csrf_token %}\n<button name='action' value='complete' class='btn btn-info'>Mark Completed</button>\n<button name='action' value='cancel' class='btn btn-secondary'>Mark Cancelled</button>\n<button name='action' value='pending' class='btn btn-warning'>Mark Pending</button>\n</form>\n</div></div>\n</div>\n</div>\n<a href='/appointments/' class='btn btn-dark mt-3'>Back to List</a>\n{% endblock %}")
apd2.close()
print('Appointment detail updated!')
login_page = open('templates/login.html','w',encoding='utf-8')
login_page.write("<!DOCTYPE html>\n<html lang='en'>\n<head>\n<meta charset='UTF-8'>\n<meta name='viewport' content='width=device-width, initial-scale=1.0'>\n<title>RadiNova AI - Login</title>\n<link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css' rel='stylesheet'>\n<link href='https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css' rel='stylesheet'>\n<style>\nbody{margin:0;padding:0;background:linear-gradient(135deg,#0f2027,#203a43,#2c5364);min-height:100vh;display:flex;align-items:center;justify-content:center;}\n.login-card{background:white;border-radius:20px;padding:40px;width:100%;max-width:420px;box-shadow:0 20px 60px rgba(0,0,0,0.4);}\n.brand-icon{background:linear-gradient(135deg,#1e3a5f,#2563eb);width:70px;height:70px;border-radius:50%;display:flex;align-items:center;justify-content:center;margin:0 auto 15px;}\n.brand-icon i{color:white;font-size:2rem;}\n.btn-login{background:linear-gradient(135deg,#1e3a5f,#2563eb);border:none;padding:12px;font-size:1rem;letter-spacing:1px;}\n.btn-login:hover{background:linear-gradient(135deg,#2563eb,#1e3a5f);}\n.form-control:focus{border-color:#2563eb;box-shadow:0 0 0 0.2rem rgba(37,99,235,0.25);}\n</style>\n</head>\n<body>\n<div class='login-card'>\n<div class='text-center mb-4'>\n<div class='brand-icon'><i class='bi bi-activity'></i></div>\n<h3 class='fw-bold text-dark'>RadiNova AI</h3>\n<p class='text-muted mb-0'>Radiology Management System</p>\n</div>\n{% if form.errors %}\n<div class='alert alert-danger py-2'><i class='bi bi-exclamation-circle'></i> Invalid username or password</div>\n{% endif %}\n<form method='post'>\n{% csrf_token %}\n<div class='mb-3'>\n<label class='form-label fw-semibold'>Username</label>\n<div class='input-group'>\n<span class='input-group-text'><i class='bi bi-person'></i></span>\n<input type='text' name='username' class='form-control' placeholder='Enter username' required autofocus>\n</div>\n</div>\n<div class='mb-4'>\n<label class='form-label fw-semibold'>Password</label>\n<div class='input-group'>\n<span class='input-group-text'><i class='bi bi-lock'></i></span>\n<input type='password' name='password' class='form-control' placeholder='Enter password' required>\n</div>\n</div>\n<button type='submit' class='btn btn-login btn-primary w-100 text-white fw-bold'>LOGIN</button>\n</form>\n<p class='text-center text-muted mt-4 mb-0' style='font-size:0.85rem;'>RadiNova AI &copy; 2026</p>\n</div>\n</body>\n</html>")
login_page.close()
print('Login page done!')# Print button - update scan_detail and report pages
print_css = "\n<style>@media print{.no-print{display:none!important;}.print-area{display:block;}}</style>\n"

# Update report detail with print button
rd = open('templates/report_detail.html','r',encoding='utf-8').read()
if 'Print' not in rd:
    rd = rd.replace("{% endblock %}", "<button onclick='window.print()' class='btn btn-success no-print mt-2'><i class='bi bi-printer'></i> Print Report</button>\n{% endblock %}")
    open('templates/report_detail.html','w',encoding='utf-8').write(rd)
    print('Print button added to report!')
else:
    print('Print already exists!')
    reg = open('templates/register.html','w',encoding='utf-8')
reg.write("<!DOCTYPE html>\n<html lang='en'>\n<head>\n<meta charset='UTF-8'>\n<meta name='viewport' content='width=device-width, initial-scale=1.0'>\n<title>RadiNova AI - Register</title>\n<link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css' rel='stylesheet'>\n<link href='https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css' rel='stylesheet'>\n<style>\nbody{margin:0;padding:0;background:linear-gradient(135deg,#0f2027,#203a43,#2c5364);min-height:100vh;display:flex;align-items:center;justify-content:center;}\n.reg-card{background:white;border-radius:20px;padding:40px;width:100%;max-width:420px;box-shadow:0 20px 60px rgba(0,0,0,0.4);}\n.brand-icon{background:linear-gradient(135deg,#1e3a5f,#2563eb);width:70px;height:70px;border-radius:50%;display:flex;align-items:center;justify-content:center;margin:0 auto 15px;}\n.brand-icon i{color:white;font-size:2rem;}\n.btn-reg{background:linear-gradient(135deg,#1e3a5f,#2563eb);border:none;padding:12px;font-size:1rem;}\n.form-control:focus{border-color:#2563eb;box-shadow:0 0 0 0.2rem rgba(37,99,235,0.25);}\n</style>\n</head>\n<body>\n<div class='reg-card'>\n<div class='text-center mb-4'>\n<div class='brand-icon'><i class='bi bi-activity'></i></div>\n<h3 class='fw-bold'>RadiNova AI</h3>\n<p class='text-muted mb-0'>Create your account</p>\n</div>\n{% if messages %}{% for message in messages %}\n<div class='alert alert-danger py-2'>{{ message }}</div>\n{% endfor %}{% endif %}\n<form method='post'>{% csrf_token %}\n<div class='mb-3'><label class='form-label fw-semibold'>Username</label>\n<div class='input-group'><span class='input-group-text'><i class='bi bi-person'></i></span>\n<input type='text' name='username' class='form-control' placeholder='Choose username' required></div></div>\n<div class='mb-3'><label class='form-label fw-semibold'>Password</label>\n<div class='input-group'><span class='input-group-text'><i class='bi bi-lock'></i></span>\n<input type='password' name='password1' class='form-control' placeholder='Enter password' required></div></div>\n<div class='mb-4'><label class='form-label fw-semibold'>Confirm Password</label>\n<div class='input-group'><span class='input-group-text'><i class='bi bi-lock-fill'></i></span>\n<input type='password' name='password2' class='form-control' placeholder='Confirm password' required></div></div>\n<button type='submit' class='btn btn-reg btn-primary w-100 text-white fw-bold'>CREATE ACCOUNT</button>\n</form>\n<p class='text-center mt-3 mb-0'>Already have an account? <a href='/login/' class='text-primary fw-semibold'>Login</a></p>\n</div></body></html>")
reg.close()
print('Register page done!')