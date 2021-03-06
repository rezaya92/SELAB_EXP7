from rest_framework import serializers
from django.contrib.auth import get_user_model # If used custom user model

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    national_id = serializers.CharField(source='username')

    def create(self, validated_data):

        user = UserModel.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            is_doctor=validated_data['is_doctor'],
            is_patient=validated_data['is_patient'],
            name=validated_data['name'],
        )

        return user

    class Meta:
        model = UserModel
        fields = ("id", "password", "is_doctor", "is_patient", "national_id", "name")
