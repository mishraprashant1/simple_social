from rest_framework.generics import CreateAPIView
from apps.user.serializers import UserSignupSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class SignUpView(CreateAPIView):
    serializer_class = UserSignupSerializer
    permission_classes = []
    authentication_classes = []
    throttle_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        account = serializer.save()
        headers = self.get_success_headers(serializer.data)
        data = dict()
        data['response'] = 'Registration Successful!'
        data['username'] = account.username
        data['email'] = account.email
        data['token'] = get_tokens_for_user(account)

        return Response(data, status=status.HTTP_201_CREATED, headers=headers)
