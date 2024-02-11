# accounts/views.py
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import DestroyAPIView
from .models import CustomUser
from .serializers import CustomUserSerializer
from rest_framework.permissions import AllowAny
from datetime import date
from .permissions import IsUserOwner
from rest_framework.permissions import IsAuthenticated
from functools import partial



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        # Ajoutez des champs personnalisés au besoin
        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        # Ajoutez des champs personnalisés au besoin
        return data

class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer

class CustomUserViewSet(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def signup_view(request):
    serializer = CustomUserSerializer(data=request.data)

    if serializer.is_valid():
        # Vérifier l'âge
        birthday = serializer.validated_data.get('birthday')
        age = (date.today() - birthday).days // 365

        if age < 15:
            return Response({'error': 'L\'utilisateur doit avoir au moins 15 ans pour s\'inscrire.'}, status=status.HTTP_400_BAD_REQUEST)

        # Créer l'utilisateur
        serializer.save()

        # Générer la réponse
        response_data = {'message': 'Inscription réussie'}
        return Response(response_data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ModifyUserView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, IsUserOwner]
    serializer_class = CustomUserSerializer

    def get_object(self):
        uuid = self.kwargs.get('uuid')
        return get_object_or_404(CustomUser, uuid=uuid)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance:
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

class DeleteUserView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsUserOwner]
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    lookup_field = 'uuid'
