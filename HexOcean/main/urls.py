from django.urls import include, path
from rest_framework import routers
from . import views
from django.views.static import serve
from django.conf import settings

router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet)
router.register(r"groups", views.GroupViewSet)
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("", include(router.urls)),
    path("images/", views.ImageList.as_view(), name=""),
    # path("images/<id>", views.ImageList.as_view(), name="binary_image"),
    path("images/<id>", views.index, name="binary_image"),
    # path("image/<path:url>/", views.ImageView.as_view(), name="image_view"),
    # path("images/<username>/tier/size/photo", views.thumbnail, name="thumbnail"),
    # path("media/<path:path>", serve, {"document_root": settings.MEDIA_ROOT}),
    path("upload/", views.ImageUpload.as_view(), name=""),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
