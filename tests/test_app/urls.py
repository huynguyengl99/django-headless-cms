from rest_framework import routers

from test_app.views import PostCMSViewSet

router = routers.SimpleRouter()
router.register(r"", PostCMSViewSet, basename="posts")

urlpatterns = router.urls
