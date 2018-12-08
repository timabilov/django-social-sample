from django.urls import path, include


urlpatterns = [
    path('v1.0/', include('api.v1.urls')),
    # There are many methods for versioning, for simple one:
    # Next(v1.1) api version refer to previous one with overriding particular
    # feature
]