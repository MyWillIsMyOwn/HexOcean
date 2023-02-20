from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet)
router.register(r"groups", views.GroupViewSet)
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("", include(router.urls)),
    path("images/", views.ImageList.as_view(), name=""),
    path("upload/", views.ImageUpload.as_view(), name=""),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
