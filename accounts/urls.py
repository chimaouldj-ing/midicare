from django.urls import path
from . import views


urlpatterns = [
    path(
        "login/",
        views.login_view,
        name="login"
    ),

    path(
        "register/",
        views.register_view,
        name="register"
    ),

    path(
        "logout/",
        views.logout_view,
        name="logout"
    ),

    path(
        "dashboard/",
        views.dashboard_view,
        name="dashboard"
    ),

    path(
        "patient/dashboard/",
        views.patient_dashboard,
        name="patient_dashboard"
    ),

    path(
        "patient/doctors/",
        views.doctors_list,
        name="doctors_list"
    ),

    path(
        "patient/book/<int:doctor_id>/",
        views.book_appointment,
        name="book_appointment"
    ),

    path(
        "patient/cancel/<int:appointment_id>/",
        views.cancel_appointment,
        name="cancel_appointment"
    ),

    path(
        "doctor/dashboard/",
        views.doctor_dashboard,
        name="doctor_dashboard"
    ),

    path(
        "admin-dashboard/",
        views.admin_dashboard,
        name="admin_dashboard"
    ),
]