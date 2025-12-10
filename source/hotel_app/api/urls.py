from django.urls import path, include
from .views import RootAPIView, RoomViewSet, BookingViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"rooms", RoomViewSet, basename="room")
router.register(r"bookings", BookingViewSet, basename="booking")

urlpatterns = [
    path("", RootAPIView.as_view(), name="api-root"),
    path("", include(router.urls))
]