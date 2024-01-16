# api/serializers.py
from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('dni', 'apel_nomb', 'tipo_usuarioapp', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        instance.apel_nomb = validated_data.get('apel_nomb', instance.apel_nomb)
        instance.tipo_usuarioapp = validated_data.get('tipo_usuarioapp', instance.tipo_usuarioapp)
        instance.save()
        return instance
