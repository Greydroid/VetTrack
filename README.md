# VetTrack API

Backend for managing animal patients, vaccinations, reminders, and roles (Admin, Vet, Receptionist).

## Run locally

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

