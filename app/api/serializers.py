from rest_framework import serializers

from app.models import DateTimeSlot, Appointment


class DateTimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = DateTimeSlot
        fields = ('id', 'appointment_date', 'start', 'end', 'status', 'created_at')


class AppointmentSerializer(serializers.ModelSerializer):
    reference_number = serializers.CharField(required=False)

    class Meta:
        model = Appointment
        fields = ('reference_number', 'slot', 'full_name', 'mobile_number',
                  'email', 'patient_type', 'status', 'created_at')

    def to_representation(self, instance):
        self.fields['slot'] = DateTimeSlotSerializer(read_only=True)
        return super(AppointmentSerializer, self).to_representation(instance)