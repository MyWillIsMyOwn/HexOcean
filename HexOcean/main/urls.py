from django.urls import include, path
from . import views


urlpatterns = [
    path("images/", views.ImageList.as_view(), name=""),
    path("images/<id>", views.index, name="binary_image"),
    path("upload/", views.ImageUpload.as_view(), name=""),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
