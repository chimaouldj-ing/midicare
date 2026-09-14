from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from datetime import date

from .models import (
    User,
    Patient,
    Doctor,
    Speciality,
    Appointment,
    MedicalRecord,
    Prescription,
    MedicalAnalysis,
    Notification,
)


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("dashboard")

        return render(
            request,
            "accounts/login.html",
            {
                "error": "Nom d'utilisateur ou mot de passe incorrect."
            }
        )

    return render(request, "accounts/login.html")


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")

        if User.objects.filter(username=username).exists():
            return render(
                request,
                "accounts/register.html",
                {
                    "error": "Ce nom d'utilisateur existe déjà."
                }
            )

        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email,
        )

        Patient.objects.create(user=user)

        login(request, user)

        return redirect("patient_dashboard")

    return render(request, "accounts/register.html")


@login_required
def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def dashboard_view(request):
    if hasattr(request.user, "patient_profile"):
        return redirect("patient_dashboard")

    if hasattr(request.user, "doctor_profile"):
        return redirect("doctor_dashboard")

    if request.user.is_superuser:
        return redirect("admin_dashboard")

    return redirect("login")


# =========================
# PATIENT
# =========================

@login_required
def patient_dashboard(request):
    try:
        patient = request.user.patient_profile
    except Patient.DoesNotExist:
        return redirect("login")

    appointments = (
        Appointment.objects
        .filter(patient=patient)
        .select_related(
            "doctor",
            "doctor__user",
            "doctor__speciality"
        )
        .order_by("-date", "-time")
    )

    try:
        medical_record = patient.medical_record
    except MedicalRecord.DoesNotExist:
        medical_record = None

    prescriptions = (
        Prescription.objects
        .filter(patient=patient)
        .prefetch_related("items")
        .order_by("-created_at")
    )

    analyses = (
        MedicalAnalysis.objects
        .filter(patient=patient)
        .select_related(
            "doctor",
            "doctor__user"
        )
        .order_by("-requested_at")
    )

    notifications = (
        Notification.objects
        .filter(user=request.user)
        .order_by("-created_at")
    )

    context = {
        "patient": patient,
        "appointments": appointments,
        "medical_record": medical_record,
        "prescriptions": prescriptions,
        "analyses": analyses,
        "notifications": notifications,
    }

    return render(
        request,
        "accounts/patient_dashboard.html",
        context
    )


@login_required
def doctors_list(request):
    if not hasattr(request.user, "patient_profile"):
        return redirect("dashboard")

    doctors = (
        Doctor.objects
        .select_related("user", "speciality")
        .all()
    )

    return render(
        request,
        "accounts/doctors.html",
        {"doctors": doctors}
    )


@login_required
def book_appointment(request, doctor_id):
    if not hasattr(request.user, "patient_profile"):
        return redirect("dashboard")

    doctor = get_object_or_404(
        Doctor,
        id=doctor_id
    )

    patient = request.user.patient_profile

    if request.method == "POST":
        appointment_date = request.POST.get("date")
        appointment_time = request.POST.get("time")

        existing_appointment = Appointment.objects.filter(
            doctor=doctor,
            date=appointment_date,
            time=appointment_time,
            status="Pending"
        ).exists()

        if existing_appointment:
            return render(
                request,
                "accounts/doctors.html",
                {
                    "doctors": Doctor.objects.select_related(
                        "user",
                        "speciality"
                    ).all(),
                    "error": (
                        "Ce médecin a déjà un rendez-vous "
                        "à cette date et cette heure."
                    ),
                }
            )

        Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            date=appointment_date,
            time=appointment_time,
            status="Pending"
        )

        Notification.objects.create(
            user=request.user,
            message=(
                f"Votre rendez-vous avec Dr. "
                f"{doctor.user.last_name} a été enregistré."
            )
        )

        return redirect("patient_dashboard")

    return redirect("doctors_list")


@login_required
def cancel_appointment(request, appointment_id):
    if not hasattr(request.user, "patient_profile"):
        return redirect("dashboard")

    patient = request.user.patient_profile

    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        patient=patient
    )

    if request.method == "POST":
        if appointment.status == "Pending":
            appointment.status = "Cancelled"
            appointment.save()

            Notification.objects.create(
                user=request.user,
                message="Votre rendez-vous a été annulé."
            )

    return redirect("patient_dashboard")


# =========================
# DOCTOR
# =========================

@login_required
def doctor_dashboard(request):
    try:
        doctor = request.user.doctor_profile
    except Doctor.DoesNotExist:
        return redirect("login")

    appointments = (
        Appointment.objects
        .filter(doctor=doctor)
        .select_related(
            "patient",
            "patient__user"
        )
        .order_by("date", "time")
    )

    today_appointments = appointments.filter(
        date=date.today()
    )

    pending_appointments = appointments.filter(
        status="Pending"
    )

    confirmed_appointments = appointments.filter(
        status="Confirmed"
    )

    completed_appointments = appointments.filter(
        status="Completed"
    )

    context = {
        "doctor": doctor,
        "appointments": appointments,
        "today_appointments": today_appointments,
        "pending_appointments": pending_appointments,
        "confirmed_appointments": confirmed_appointments,
        "completed_appointments": completed_appointments,
    }

    return render(
        request,
        "accounts/doctor_dashboard.html",
        context
    )


@login_required
def update_appointment_status(request, appointment_id):
    try:
        doctor = request.user.doctor_profile
    except Doctor.DoesNotExist:
        return redirect("login")

    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        doctor=doctor
    )

    if request.method == "POST":
        new_status = request.POST.get("status")

        allowed_statuses = [
            "Pending",
            "Confirmed",
            "Completed",
            "Cancelled",
        ]

        if new_status in allowed_statuses:
            appointment.status = new_status
            appointment.save()

            Notification.objects.create(
                user=appointment.patient.user,
                message=(
                    f"Le statut de votre rendez-vous avec "
                    f"Dr. {doctor.user.last_name} a été changé en "
                    f"{new_status}."
                )
            )

    return redirect("doctor_dashboard")


# =========================
# ADMIN
# =========================

@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect("dashboard")

    context = {
        "users_count": User.objects.count(),
        "doctors_count": Doctor.objects.count(),
        "patients_count": Patient.objects.count(),
        "appointments_count": Appointment.objects.count(),
    }

    return render(
        request,
        "accounts/admin_dashboard.html",
        context
    )