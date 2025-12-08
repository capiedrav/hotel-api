from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from ..models import Room
from .serializers import RoomSerializer

# Create your views here.

class RootAPIView(APIView):

    def get(self, request):

        return Response({"message": "Hello, World!"})


class RoomViewSet(viewsets.ModelViewSet):

    queryset = Room.objects.all()
    serializer_class = RoomSerializer