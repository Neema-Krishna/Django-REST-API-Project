from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from user_app.api.serializers import RegistrationSerailizer
from django.contrib.auth.models import User
from user_app import models


class LogOutView(APIView):
    def post(self,request):
        request.user.auth_token.delete()
        return Response(data='Logged Out',status=status.HTTP_200_OK)


class RegistrationView(APIView):
    def post(self,request,*args,**kwargs):
        serializer=RegistrationSerailizer(data=request.data)
        data={}
        if serializer.is_valid():
            account=serializer.save()
            data['response']='Reg successfull'
            data['username']=account.username
            data['email']=account.email
            # JWT TOKEN
            # refresh = RefreshToken.for_user(account)
            # data['token']= {
                        # 'refresh': str(refresh),
                        # 'access': str(refresh.access_token),
                        #  }
            
            token=Token.objects.get(user=account).key
            data['token']=token
        else:
            data=serializer.errors
        return Response(data,status=status.HTTP_201_CREATED)
       
            
        
     