from django.urls import path, include

from app.api.routers import router


from app import views

urlpatterns = [
    path('', views.landingpage, name="landing_page"),
    path('management', views.admin_dashboard, name="admin_dashboard"),
    path('api/', include(router.urls)),
]