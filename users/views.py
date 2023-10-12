from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import User
from users.serializers import RegisterSerializer, MyTokenObtainPairSerializer
from rest_framework import generics


class RegisterAPIView(generics.CreateAPIView):
    """Контроллер для регистрации нового пользователя"""
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    """Контроллер для получения JWT-токена"""
    serializer_class = MyTokenObtainPairSerializer

