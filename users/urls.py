from .views import UserViewSet
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import SimpleRouter  # we can use custom routers
from django.urls import path

router = SimpleRouter()
router.register('user', UserViewSet)

urlpatterns = router.urls

