# accounts/serializers.py
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import CustomUser

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        # Ajoutez des champs personnalisés si nécessaire
        data['username'] = self.user.username
        return data

class CustomUserSerializer(serializers.ModelSerializer):
    birthday = serializers.DateField(write_only=True)  # Ajoutez cette ligne pour le champ de date de naissance

    class Meta:
        model = CustomUser
        fields = ['uuid', 'username', 'email', 'password', 'birthday']  # Ajoutez les champs appropriés
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user