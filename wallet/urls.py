from .views import UserWalletViewSet , start_payment , handle_payment_success , PaymentViewSet
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import SimpleRouter  # we can use custom routers
from django.urls import path

router = SimpleRouter()
router.register('user_wallet', UserWalletViewSet)
router.register('transaction', PaymentViewSet)


urlpatterns = [
    path('pay/', start_payment, name="payment"),
    path('payment/success/', handle_payment_success)
]
urlpatterns.extend(router.urls)

