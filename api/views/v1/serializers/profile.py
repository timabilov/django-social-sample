from django.contrib.auth import password_validation
from django.contrib.auth.hashers import make_password

from rest_framework import serializers

from api.models import UserProfile


class UserRegistrationSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(required=False)

    class Meta:
        model = UserProfile
        fields = ('username', 'password', 'email')

    def validate_password(self, data):
        # AUTH_PASSWORD_VALIDATORS does the job.
        password_validation.validate_password(password=data, user=UserProfile)
        return make_password(data)
