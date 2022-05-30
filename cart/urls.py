from .views import ItemViewSet ,CartViewSet
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import SimpleRouter  # we can use custom routers
from django.urls import path

router = SimpleRouter()
router.register('item', ItemViewSet)
router.register('cart', CartViewSet)

urlpatterns = router.urls

