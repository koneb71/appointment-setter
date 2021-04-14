from datetime import datetime
import logging
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from app.api.serializers import DateTimeSlotSerializer, AppointmentSerializer
from app.models import DateTimeSlot, Appointment


class DateTimeSlotView(viewsets.ModelViewSet):
    serializer_class = DateTimeSlotSerializer
    queryset = DateTimeSlot.objects.all()

    @action(detail=False)
    def available(self, request):
        dates = DateTimeSlot.objects.filter(appointment_date__gt=datetime.now().date()) \
            .filter(status=0).values_list('appointment_date', flat=True).distinct()
        return Response(list(dates))

    @action(detail=False)
    def slots(self, request, *args, **kwargs):
        selected_date = request.GET.get('date')
        if not selected_date:
            return Response([])

        querysets = DateTimeSlot.objects.filter(appointment_date=selected_date) \
                                        .filter(status=0)
        serializer = self.get_serializer(querysets, many=True)
        return Response(serializer.data)


class AppointmentView(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.all()