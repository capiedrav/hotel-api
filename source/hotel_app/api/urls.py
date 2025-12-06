from django.urls import path
from .views import RootAPIView

urlpatterns = [
    path("", RootAPIView.as_view(), name="root"),
]