from django.urls import path, include

from app.api.routers import router


from app import views

urlpatterns = [
    path('', views.landingpage, name="landing_page"),
    path('api/', include(router.urls)),
]