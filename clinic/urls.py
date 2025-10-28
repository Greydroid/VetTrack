from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()
router.register(r"api/animals", views.AnimalViewSet, basename="animals")
router.register(r"api/vaccinations", views.VaccinationViewSet, basename="vaccinations")
router.register(r"api/reminders", views.ReminderViewSet, basename="reminders")
router.register(r"api/users", views.UserViewSet, basename="users")

urlpatterns = [
    path("", include(router.urls)),
]
