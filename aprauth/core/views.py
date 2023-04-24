from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import UserSerializer

# Create your views here.


class RegisterView(APIView):
    permission_classes = [AllowAny,]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)
    
    def get(self,request):
        return Response({"detail":"success"}, status=HTTP_200_OK)
    
class UserApiView(RetrieveAPIView):
    
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
    
