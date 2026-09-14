from django.contrib import admin
from .models import (
    User,
    Patient,
    Doctor,
    Speciality,
    Appointment,
    MedicalRecord,
    Consultation,
    Prescription,
    PrescriptionItem,
    MedicalAnalysis,
    AnalysisResult,
    Notification,
)


# ============================================================
# USER
# ============================================================

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "is_staff",
        "is_active",
    )
    search_fields = (
        "username",
        "first_name",
        "last_name",
        "email",
    )


# ============================================================
# SPECIALITY
# ============================================================

@admin.register(Speciality)
class SpecialityAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


# ============================================================
# PATIENT
# ============================================================

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "phone",
        "date_of_birth",
        "address",
    )
    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
        "phone",
    )


# ============================================================
# DOCTOR
# ============================================================

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "speciality",
        "phone",
    )
    list_filter = ("speciality",)
    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
        "phone",
    )


# ============================================================
# APPOINTMENT
# ============================================================

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        "patient",
        "doctor",
        "date",
        "time",
        "status",
        "created_at",
    )
    list_filter = (
        "status",
        "date",
        "doctor",
    )
    search_fields = (
        "patient__user__username",
        "doctor__user__username",
    )
    ordering = ("-date", "-time")


# ============================================================
# MEDICAL RECORD
# ============================================================

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = (
        "patient",
        "blood_type",
        "allergies",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "patient__user__username",
        "blood_type",
        "allergies",
    )


# ============================================================
# CONSULTATION
# ============================================================

@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = (
        "patient",
        "doctor",
        "appointment",
        "diagnosis",
        "created_at",
    )
    list_filter = (
        "doctor",
        "created_at",
    )
    search_fields = (
        "patient__user__username",
        "doctor__user__username",
        "diagnosis",
    )


# ============================================================
# PRESCRIPTION
# ============================================================

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = (
        "patient",
        "doctor",
        "consultation",
        "created_at",
    )
    list_filter = (
        "doctor",
        "created_at",
    )
    search_fields = (
        "patient__user__username",
        "doctor__user__username",
    )


# ============================================================
# PRESCRIPTION ITEM
# ============================================================

@admin.register(PrescriptionItem)
class PrescriptionItemAdmin(admin.ModelAdmin):
    list_display = (
        "prescription",
        "medication_name",
        "dosage",
        "frequency",
        "duration",
    )
    search_fields = (
        "medication_name",
        "dosage",
    )


# ============================================================
# MEDICAL ANALYSIS
# ============================================================

@admin.register(MedicalAnalysis)
class MedicalAnalysisAdmin(admin.ModelAdmin):
    list_display = (
        "patient",
        "doctor",
        "analysis_type",
        "status",
        "requested_at",
    )
    list_filter = (
        "status",
        "analysis_type",
        "doctor",
    )
    search_fields = (
        "patient__user__username",
        "doctor__user__username",
        "analysis_type",
    )


# ============================================================
# ANALYSIS RESULT
# ============================================================

@admin.register(AnalysisResult)
class AnalysisResultAdmin(admin.ModelAdmin):
    list_display = (
        "analysis",
        "result_date",
    )
    search_fields = (
        "analysis__analysis_type",
        "result",
    )


# ============================================================
# NOTIFICATION
# ============================================================

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "title",
        "is_read",
        "created_at",
    )
    list_filter = (
        "is_read",
        "created_at",
    )
    search_fields = (
        "user__username",
        "title",
        "message",
    )