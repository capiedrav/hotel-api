from django.urls import path
from .views import RootAPIView, RoomListAPIView

urlpatterns = [
    path("", RootAPIView.as_view(), name="api-root"),
    path("rooms/", RoomListAPIView.as_view(actions={"get": "list"}), name="list-rooms"),
]