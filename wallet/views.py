from rest_framework import viewsets
from rest_framework import status
import datetime
from .serializers import UserWalletSerializer , PaymentSerializer
from .permissions import IsUser ,IsOnBoard ,ReadOnly
from django.contrib.auth.models import User
from wallet.models import UserWallet , Payment
from django.contrib.auth.mixins import LoginRequiredMixin  # we cannot user @login_requried decorators  on class views
from django.contrib.auth.mixins import UserPassesTestMixin
from rest_framework.response import Response
from rest_framework.decorators import action ,api_view
import json
import razorpay
from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as filters
import os


with open(r'C:\Users\Avinash vishwakarma\Desktop\blog_config.json') as config_file:
    config = json.load(config_file)
    
################## django api view ###################


class UserWalletViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated,]
    queryset = UserWallet.objects.all()
    serializer_class = UserWalletSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('user', )

    
    @action(methods=['put'], detail=True, permission_classes=[IsAuthenticated,],url_path='purchased', url_name='purchased')
    def purchased(self, request, pk=None):
        '''  Description : purchased method will be used for debit purpose from wallet 
                       it will check that requested user have enough amount to make the transaction or not '''
        req_user_wallet = UserWallet.objects.get(user = request.user)
       
        # if requested amount is suffiecient enough then current balance/amount will be updated
        if int(request.data['cur_balance']) <= req_user_wallet.cur_balance :
            req_user_wallet.cur_balance -= int(request.data['cur_balance'])

            req_user_wallet.save()
            return Response(status = status.HTTP_201_CREATED)
        else :
            return Response(status = status.HTTP_400_BAD_REQUEST)    

#*******************************************************|||***************************************************************#        
    
################################# payment gateway integration using razorpay #####################################

# reference : https://blog.learncodeonline.in/how-to-integrate-razorpay-payment-gateway-with-django-rest-framework-and-reactjs

@api_view(['POST'])
def start_payment(request):
    # print(request.data)
    # request.data is coming from frontend
    amount = request.data['ammount']
    payment_type = request.data['payment_type']
    # setup razorpay client this is the client to whome user is paying money that's you
      
    #client = razorpay.Client(auth=(env('PUBLIC_KEY'), env('SECRET_KEY')))
    client = razorpay.Client(auth=(os.environ['PUBLIC_KEY'], os.environ['SECRET_KEY']))
    # create razorpay order
    # the amount will come in 'paise' that means if we pass 50 amount will become
    # 0.5 rupees that means 50 paise so we have to convert it in rupees. So, we will 
    # mumtiply it by 100 so it will be 50 rupees.
    payment = client.order.create({"amount": int(amount) * 100, 
                                   "currency": "INR", 
                                   "payment_capture": "1"})

    # we are saving an order with isPaid=False because we've just initialized the order
    # we haven't received the money we will handle the payment succes in next 
    # function
    payment_obj = Payment.objects.create(user = request.user, # we need to decide what it should be 
                                        payment_amount=amount, 
                                        payment_id=payment['id'],
                                        payment_date = datetime.datetime.now() ,
                                        payment_type = payment_type)
 
    serializer = PaymentSerializer(payment_obj)

    '''payment response will be 
    {'id': 17, 
    'payment_date': '23 January 2021 03:28 PM', 
    'user': '** user inititatiing payment from frontend**', 
    'payment_amount': '**amount from frontend**', 
    'payment_id': 'order_G3NhfSWWh5UfjQ', # it will be unique everytime
    'isPaid': False}'''
    # print(serializer.data)
    data = {
        "payment": payment,
        "order": serializer.data
    }
    print("payment initiated")
    return Response(data)


@api_view(['POST'])
def handle_payment_success(request):
    # request.data is coming from frontend
   
    res = request.data["response"]
    
    '''res will be:
    {'razorpay_payment_id': 'pay_G3NivgSZLx7I9e', 
    'razorpay_order_id': 'order_G3NhfSWWh5UfjQ', 
    'razorpay_signature': '76b2accbefde6cd2392b5fbf098ebcbd4cb4ef8b78d62aa5cce553b2014993c0'}
    this will come from frontend which we will use to validate and confirm the payment
    '''

    ord_id = ""
    raz_pay_id = ""
    raz_signature = ""

    # res.keys() will give us list of keys in res
    for key in res.keys():
        if key == 'razorpay_order_id':
            ord_id = res[key]
        elif key == 'razorpay_payment_id':
            raz_pay_id = res[key]
        elif key == 'razorpay_signature':
            raz_signature = res[key]

    # get order by payment_id which we've created earlier with isPaid=False
    order = Payment.objects.get(payment_id=ord_id)

    # we will pass this whole data in razorpay client to verify the payment
    data = {
        'razorpay_order_id': ord_id,
        'razorpay_payment_id': raz_pay_id,
        'razorpay_signature': raz_signature
    }
    print(data)
    client = razorpay.Client(auth=(config['PUBLIC_KEY'], config['SECRET_KEY']))
    # checking if the transaction is valid or not by passing above data dictionary in 
    # razorpay client if it is "valid" then check will return None
    check = client.utility.verify_payment_signature(data)
    print(data , check)

    if check is not None:
        print("Redirect to error url or error page")
        return Response({'error': 'Something went wrong'},status= status.HTTP_400_BAD_REQUEST)

    # if payment is successful that means check is None then we will turn isPaid=True
    if order.payment_type == "cart":
        cart = Cart.objects.filter(user = order.user , price = order.payment_amount , paid=False)
        cart = cart[0]
        cart.paid = True
        cart.save()
    else :    
        order.isPaid = True
        user_wallet_obj = UserWallet.objects.get(user = order.user)
        user_wallet_obj.cur_balance += order.amount # adding balance to the user account
        user_wallet_obj.save()
        order.save()

    res_data = {
        'message': 'payment successfully received!'
    }

    return Response(res_data, status=status.HTTP_201_CREATED )
    

class PaymentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsUser]
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('user', )


