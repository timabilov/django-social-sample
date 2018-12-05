from django.contrib.auth import password_validation
from django.contrib.auth.hashers import make_password

from rest_framework import serializers

from api.models import UserProfile


class UserRegistrationSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(required=False)

    class Meta:
        model = UserProfile
        fields = ('username', 'password', 'email')

    # TODO:
    # we can use emailhunter.co API right here to validate email as one solution
    # def validate_email -> check from API

    def validate_password(self, data):
        # AUTH_PASSWORD_VALIDATORS does the job.
        password_validation.validate_password(password=data, user=UserProfile)
        return make_password(data)
