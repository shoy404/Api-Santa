from django.contrib.auth import authenticate
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

from .models import CustomUser
from .serializers import CustomUserSerializer

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        # Usar AllowAny solo para la acción 'create'
        if self.action == 'create':
            self.permission_classes = [AllowAny]

        return super().get_permissions()

    def perform_create(self, serializer):
        # Guarda el nuevo usuario
        user = serializer.save()

        # Genera un token para el usuario
        refresh = RefreshToken.for_user(user)

        # Agrega el token a la respuesta
        response_data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        return Response(response_data, status=status.HTTP_201_CREATED)

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()

class ObtainTokenView(APIView):
    def post(self, request):
        dni = request.data.get('dni')
        password = request.data.get('password')

        user = authenticate(request, dni=dni, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)
