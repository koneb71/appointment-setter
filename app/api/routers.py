from rest_framework import routers

from app.api.viewsets import DateTimeSlotView, AppointmentView

router = routers.DefaultRouter()
router.register(r'dates', DateTimeSlotView)
router.register(r'appointment', AppointmentView)