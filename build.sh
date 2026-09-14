#!/usr/bin/env bash

python manage.py collectstatic --no-input
python manage.py migrate

python manage.py shell <<'PY'
from accounts.models import User, Doctor, Speciality

user, created = User.objects.get_or_create(
    username="doctor1",
    defaults={
        "first_name": "Doctor",
        "last_name": "Test",
    }
)

user.set_password("Doctor12345")
user.save()

speciality, _ = Speciality.objects.get_or_create(name="Cardiology")

Doctor.objects.get_or_create(
    user=user,
    defaults={
        "speciality": speciality,
        "phone": "0550000000",
    }
)
PY