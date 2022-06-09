from rest_framework import viewsets
from .serializers import UserSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action ,api_view
import datetime
from django.shortcuts import get_list_or_404, get_object_or_404
from django.db.models import Count,Max,Sum
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from django_filters import rest_framework as filters
from rest_framework.parsers import JSONParser,MultiPartParser,FileUploadParser


User = get_user_model()

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

