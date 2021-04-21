from django.shortcuts import render, redirect
from django.urls import reverse

from app.models import Appointment


def landingpage(request):
    ctx = dict(
        title="Welcome!"
    )
    return render(request, 'landingpage/index.html', ctx)


def admin_dashboard(request):
    return redirect(reverse('appointments'))
    # ctx = dict(
    #     title="Admin Portal"
    # )
    # return render(request, 'portal/index.html', ctx)


def appointments(request):
    items = Appointment.objects.all().order_by('-created_at')
    ctx = dict(
        title="Appointments",
        items=items,
        nav='appointments'
    )
    return render(request, 'portal/appointments.html', ctx)


def calendar(request):
    ctx = dict(
        title="Calendar",
        nav='calendar'
    )
    return render(request, 'portal/calendar.html', ctx)