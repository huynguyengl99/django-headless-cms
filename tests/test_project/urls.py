from django.contrib import admin
from django.urls import include, path

admin.autodiscover()

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("martor.urls")),
    path("test-app/", include("test_app.urls")),
]
