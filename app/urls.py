from django.urls import path, include

from app.api.routers import router


from app import views

urlpatterns = [
    path('', views.landingpage, name="landing_page"),
    path('management', views.admin_dashboard, name="admin_dashboard"),
    path('appointments', views.appointments, name="appointments"),
    path('calendar', views.calendar, name="calendar"),
    path('api/', include(router.urls)),
]