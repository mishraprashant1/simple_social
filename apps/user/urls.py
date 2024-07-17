from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from apps.user.api.signup import SignUpView

urlpatterns = [
    path('api/signin/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/signin/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/signin/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/signup/', SignUpView.as_view(), name='signup'),
]
