from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from user.api.serializers import RegisterationSerializer


class Register(APIView):
    def post(self, request):
        serializer = RegisterationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()  # save method in serializer returns the user object
            data['response'] = 'Successfully registered a new user.'
            data['username'] = account.username
            data['email'] = account.email

            token, created = Token.objects.get_or_create(user=account)
            data['token'] = token.key
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data = serializer.errors
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class RegisterWithJWT(APIView):
    def post(self, request):
        serializer = RegisterationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()  # save method in serializer returns the user object
            data['response'] = 'Successfully registered a new user.'
            data['username'] = account.username
            data['email'] = account.email

            from rest_framework_simplejwt.tokens import RefreshToken
            refresh = RefreshToken.for_user(account)
            data['token'] = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }

            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data = serializer.errors
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class Logout(APIView):
    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
