from rest_framework import ( generics, status )
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import authentication
from account.serializers import RegistrationSerializer, BlackListSerializer, LoginSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from account.renderer import UserJSONRenderer
from account.models import User


class RegistrationAPIView(generics.GenericAPIView):
    """Register new users."""
    serializer_class = RegistrationSerializer
    renderer_classes = (UserJSONRenderer,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        response = {
            "data": {
                "user": dict(user_data),
                "message": "Hello, You have successfully created an account with Fusion Camp",
                "status": "success"
            }
        }
        return Response(response, status=status.HTTP_201_CREATED)


class LoginAPIView(generics.GenericAPIView):
    """login a user via email"""
    serializer_class = LoginSerializer
    renderer_classes = (UserJSONRenderer,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.data
        response = {
            "data": {
                "user": dict(user_data),
                "message": "Hello, You have successfully logged in",
                "status": "success"
            }
        }
        return Response(response, status=status.HTTP_200_OK)

class LogoutView(generics.CreateAPIView):
    """
    This class deals with logging out a user by
    blacklisting a user token
    """
    serializer_class = BlackListSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, **args):
        """
        This method blacklists a user token
        """

        auth_header = authentication.get_authorization_header(request).split()
        token = auth_header[1].decode('utf-8')
        data = {'token': token}

        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                'data':
                    {"message": "Hello, You have successfully logged out"}
            },
            status=status.HTTP_200_OK
        )
        