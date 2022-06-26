from rest_framework import viewsets
from .serializers import ItemSerializer ,CartSerializer
from .models import Item, Cart, Otp 
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action ,api_view
import datetime
from django.shortcuts import get_list_or_404, get_object_or_404
from django.db.models import Count,Max,Sum
from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as filters
import random as r

# function for otp generation
def otpgen():
    otp=""
    for i in range(4):
        otp+=str(r.randint(1,9))
    return otp



class ItemViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    


class CartViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ['user']


    @action(detail=False, methods=['post'], url_path='add_item', url_name='add_item')
    def add_to_cart(self,request ,pk=None,*args, **kwargs):
        try :
            cart = Cart.objects.get(user=request.user,paid=False)
        except :
             cart = Cart.objects.create(user=request.user)
        cart = Cart.objects.get(user=request.user,paid=False)

        item_id     = request.query_params['item_id']
        item        = Item.objects.get(id = item_id)
        item_price  = item.price
        cart.price  = cart.price+item_price
        cart.items.add(item)
        cart.save()
        message = {'msg': 'item added successfully'}    
        return Response(message , status=status.HTTP_202_ACCEPTED)



    @action(detail=False, methods=['get'], url_path='get_mycart', url_name='get_mycart')
    def get_cart(self,request,pk=None,*args , **kwargs)   :
        user = request.user
        carts = Cart.objects.filter(user=user,proccessed = False,paid=False)
        if len(carts)==0 :
            carts = Cart.objects.create(user=user)
        serializer = self.get_serializer(carts, many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)
    


    @action(detail=False, methods=['post'] , url_path='remove_item', url_name='remove_item')
    def remove_from_cart(self,request ,pk=None,*args, **kwargs):
        cart_id = request.query_params['cart_id']

        if cart_id != "null":
            queryset    = Cart.objects.all()
            cart        = get_object_or_404(queryset, pk=cart_id)
        else :
            pass
        item_id     = request.query_params['item_id']
        item        = Item.objects.get(id = item_id)
        item_price  = item.price
        cart.price  = cart.price-item_price
        cart.items.remove(item)
        cart.save()
        message = {'msg': 'item removed successfully'}
        return Response(message , status=status.HTTP_202_ACCEPTED)

    @action(detail=False, methods=['post'] , url_path='activate_cart_req', url_name='activate_cart_req')
    def activate_cart_req(self, request, *args, **kwargs):
        cart_id = request.query_params['cart_id']
        otp = otpgen()
        cart = Cart.object.get(id = cart_id)
        otp_obj = Otp.objects.create(cart = cart, otp = otp)
        message = {'msg': 'otp created successfully'}
        return Response(message , status=status.HTTP_202_ACCEPTED)

    @action(detail=False, methods=['post'] , url_path='activate_cart', url_name='activate_cart')
    def activate_cart(self, request, *args, **kwargs):
        cart_id = request.query_params['cart_id']
        otp = request.query_params['otp']
        otp_obj = Otp.objects.get(cart_id = cart_id)
        if otp == otp_obj.otp :
            message = {'msg': 'otp matched successfully'}
            return Response(message , status=status.HTTP_202_ACCEPTED)
        else :
            message = {'msg': 'otp doesnt matched'}
            return Response(message , status=status.HTTP_400_BAD_REQUEST)
  
