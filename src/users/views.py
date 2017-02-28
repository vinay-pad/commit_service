from rest_framework import generics
from users.models import User
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
class UserAuth(generics.GenericAPIView):

    def get(self, serializer):
        username = self.request.query_params.get('username', None)
        pwd = self.request.query_params.get('password', None)
        if username and pwd:
            try:
                user = User.objects.get(username=username)
                if user and user.check_password(pwd):
                    res = { "token" : user.auth_token.key }
                    return Response(res)
            except ObjectDoesNotExist:
                return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"error": "Invalid query_params"}, status=status.HTTP_400_BAD_REQUEST)
