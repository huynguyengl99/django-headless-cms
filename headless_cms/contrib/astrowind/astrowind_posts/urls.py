from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import AWCategoryViewSet, AWPostCMSViewSet, AWPostTagViewSet

router = SimpleRouter()
router.register(r"posts", AWPostCMSViewSet)
router.register(r"tags", AWPostTagViewSet)
router.register(r"categories", AWCategoryViewSet)
urlpatterns = [path("", include(router.urls))]
