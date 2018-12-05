from django.urls import path, include

from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


# TODO pretend that there  is swagger route.


from api.views.v1.views.profile import UserSignUpAPI
from api.views.v1.views.social import PostViewSet

router = SimpleRouter()
router.register(
    'posts',
    PostViewSet,
    base_name='post'
)

urlpatterns = [
    path(
        r'token/', TokenObtainPairView.as_view(), name='token_obtain_pair'
    ),
    path(
        r'token/refresh/', TokenRefreshView.as_view(), name='token_refresh'
    ),
    path('signup/', UserSignUpAPI.as_view(), name='sign-up'),
    path('', include(router.urls)),
]
