from rest_framework import serializers
from .models import Animal, Vaccination, Reminder, User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name", "role", "password", "date_joined")
        read_only_fields = ("id", "date_joined")

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = ("id", "name", "species", "breed", "age", "owner_name", "created_at")
        read_only_fields = ("id", "created_at")


class VaccinationSerializer(serializers.ModelSerializer):
    animal = serializers.PrimaryKeyRelatedField(queryset=Animal.objects.all())

    class Meta:
        model = Vaccination
        fields = ("id", "animal", "vaccine_name", "date_administered", "next_due_date", "notes", "created_at")
        read_only_fields = ("id", "created_at")


class ReminderSerializer(serializers.ModelSerializer):
    animal = serializers.PrimaryKeyRelatedField(queryset=Animal.objects.all())
    vaccination = serializers.PrimaryKeyRelatedField(queryset=Vaccination.objects.all(), allow_null=True, required=False)

    class Meta:
        model = Reminder
        fields = ("id", "animal", "vaccination", "reminder_date", "is_sent", "created_at")
        read_only_fields = ("id", "created_at")
