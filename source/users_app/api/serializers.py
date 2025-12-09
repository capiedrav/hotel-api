from rest_framework.serializers import ModelSerializer
from ..models import CustomUser

class UserSerializer(ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}
