from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Animal, Vaccination, Reminder, User
from .serializers import AnimalSerializer, VaccinationSerializer, ReminderSerializer, UserSerializer
from .permissions import RoleBasedPermission

class AnimalViewSet(viewsets.ModelViewSet):
    queryset = Animal.objects.all().order_by("-created_at")
    serializer_class = AnimalSerializer
    permission_classes = [IsAuthenticated, RoleBasedPermission]
    basename = "animals"

class VaccinationViewSet(viewsets.ModelViewSet):
    queryset = Vaccination.objects.all().order_by("-date_administered")
    serializer_class = VaccinationSerializer
    permission_classes = [IsAuthenticated, RoleBasedPermission]
    basename = "vaccinations"

class ReminderViewSet(viewsets.ModelViewSet):
    queryset = Reminder.objects.all().order_by("-reminder_date")
    serializer_class = ReminderSerializer
    permission_classes = [IsAuthenticated, RoleBasedPermission]
    basename = "reminders"

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, RoleBasedPermission]
    basename = "users"
