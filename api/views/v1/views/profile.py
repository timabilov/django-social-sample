from django.http import JsonResponse
from rest_framework.views import APIView
from django.utils.translation import gettext_lazy as _

from api.views.v1.serializers.profile import UserRegistrationSerializer


class UserSignUpAPI(APIView):

    permission_classes = ()

    def post(self, request):

        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            if user.email:
                user.clearbit_api_sync()

            return JsonResponse({"message": _("Registered successfully.")})
        else:
            return JsonResponse(serializer.errors, status=400)
