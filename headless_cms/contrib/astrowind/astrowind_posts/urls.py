from rest_framework.routers import DefaultRouter

from .views import AWPostCMSViewSet

router = DefaultRouter()
router.register(r"", AWPostCMSViewSet, basename="posts")
urlpatterns = router.urls
