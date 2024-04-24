from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import AWPostCMSViewSet

router = SimpleRouter()
router.register(r"", AWPostCMSViewSet)
urlpatterns = [path("", include(router.urls))]
