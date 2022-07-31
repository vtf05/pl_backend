from rest_framework import viewsets
from .serializers import UserSerializer
from rest_framework import status
import json
from rest_framework.response import Response
from rest_framework.decorators import action ,api_view, permission_classes
import datetime
import math, random
from django.shortcuts import get_list_or_404, get_object_or_404
from django.db.models import Count,Max,Sum
from rest_framework.permissions import IsAuthenticated , AllowAny
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from django_filters import rest_framework as filters
from rest_framework.parsers import JSONParser,MultiPartParser,FileUploadParser
from rest_framework.authtoken.models import Token
from .models import UserOtp
import os
import environ
import requests


User = get_user_model()
env = environ.Env()
environ.Env.read_env()
class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset         =  User.objects.all()
    serializer_class =  UserSerializer

    # filter_backends  =  (filters.DjangoFilterBackend,)
    # filterset_fields =  ('mobile', 'username',)


    def get_queryset(self):
        '''
        Override method to apply required filters.
        Override is better because we have to process the string coming in.
        '''
        qs = super().get_queryset()
        try :
            mobile_no = self.request.query_params['mobile']
            mobile_no = "+91"+mobile_no
            return qs.filter(mobile=mobile_no)
        except :
            return qs    

def generateOTP() :
 
    digits = "0123456789"
    OTP = ""
    for i in range(6) :
        OTP += digits[math.floor(random.random() * 10)]
    return OTP


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request) :
    if request.method == 'POST' :
        otp = generateOTP()
          
        try :
            print(request.data)
            user,res = User.objects.get_or_create(mobile = request.data['mobile'])
            otp_obj,res = UserOtp.objects.get_or_create(user = user)
            otp_obj.otp = otp
            otp_obj.save()
            mobile_number = request.data['mobile'][3:]
            url = "https://www.fast2sms.com/dev/bulkV2"
            payload = f"variables_values={otp}&route=otp&numbers={mobile_number}"
            headers = {
                'authorization': os.environ['fast_api'],
                'Content-Type': "application/x-www-form-urlencoded",
                'Cache-Control': "no-cache",
                }
  
            response = requests.request("POST", url, data=payload, headers=headers)
            print(response.text)

        except :
            return Response (status = status.HTTP_400_BAD_REQUEST)
        try :
            token = Token.objects.create(user=user)
        except :
            token = Token.objects.get(user=user)

       
        return Response({"message": "OTP SENT"})


@api_view(['POST'])
@permission_classes([AllowAny])
def verify(request):
    if request.method == 'POST':
        user = User.objects.get(mobile = request.data['mobile'])
        otp_obj = UserOtp.objects.get(user=user)
        otp = otp_obj.otp
        if otp == int(request.data['otp']):
            try :
                token = Token.objects.create(user=user)
            except :
                token = Token.objects.get(user=user)

            response_data ={'token' : token.key}
            print('print token' , token.key)
        else :
            return Response({"message": "Wrong OTP entered !", "data": request.data}, status=status.HTTP_400_BAD_REQUEST)

        return Response(json.dumps(response_data))
