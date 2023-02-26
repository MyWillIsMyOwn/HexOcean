from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.views import View
import requests
from .serializers import ImageSerializer
from .models import Image, Tier
from rest_framework import generics, permissions, status
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
import magic, base64, os
from django.http import HttpResponse
from imagekit.processors import ResizeToFill
from django.conf import settings
from imagekit import ImageSpec
import time


class ImageView(View):
    def get(self, request, *args, **kwargs):
        url = kwargs.get("url")
        response = requests.get(url)
        image_content = response.content
        return HttpResponse(image_content, content_type="image/jpeg")


class Thumbnail(ImageSpec):
    format = "JPEG"
    options = {"quality": 90}

    def __init__(self, height, width, *args, **kwargs):
        super(type(self), self).__init__(*args, **kwargs)
        self.processors = [ResizeToFill(height=height, width=width)]


class ImageList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ImageSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        return context

    def get_queryset(self):
        return Image.objects.filter(owner=self.request.user)


class ImageUpload(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = [FileUploadParser]

    def post(self, request):
        uploaded_photo = request.data["file"]

        mime = magic.Magic(mime=True)
        uploaded_photo_mime = mime.from_buffer(uploaded_photo.read())
        if uploaded_photo_mime not in ["image/jpeg", "image/png"]:
            return Response(
                {"error": "Wrong file type. Only JPEG and PNG are allowed."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        owner = request.user
        image_object = Image(
            owner=owner,
            picture=uploaded_photo,
            name=str(uploaded_photo),
            binary_image=base64.b64encode((request.FILES["file"]).read()),
        )
        image_object.save()
        list_of_custom_tiers = Tier.objects.all()
        create_dirs(list_of_custom_tiers)
        thumbnails_data = generate_thumbnail(list_of_custom_tiers, image_object)
        image_object.thumbnails_data = thumbnails_data
        image_object.save()
        print(image_object)
        # time.sleep(1)
        serializer = ImageSerializer(image_object)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


def index(request, id):
    image = Image.objects.get(id=id)
    link_date_expiration = (
        image.link_date_expiration + timedelta(minutes=30)
    ).strftime("%m/%d/%Y %H:%M:%S")
    current_time = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    if current_time > link_date_expiration:
        return HttpResponse("<h1>Link has expired</h1>")
    return HttpResponse(f"{(image.binary_image)}")


def create_dirs(tiers):
    all_users = User.objects.all()
    for user in all_users:
        user_folder_for_thumbnails = os.path.join(settings.MEDIA_ROOT, user.username)
        if not os.path.exists(user_folder_for_thumbnails):
            os.makedirs(user_folder_for_thumbnails)
        for tier in tiers:
            tier_folder_for_thumbnails = os.path.join(
                user_folder_for_thumbnails, tier.name
            )
            if not os.path.exists(tier_folder_for_thumbnails):
                os.makedirs(tier_folder_for_thumbnails)
            for tier_lvl in tier.thumbnails["thumbnails"]:
                tier_lvl_folder = os.path.join(
                    tier_folder_for_thumbnails, tier_lvl["name"]
                )
                if not os.path.exists(tier_lvl_folder):
                    os.makedirs(tier_lvl_folder)


def generate_thumbnail(tiers, picture):
    list_of_sizes_and_url = []
    image_source = settings.MEDIA_ROOT + "images/" + picture.name
    for tier in tiers:
        for thumbnails in tier.thumbnails["thumbnails"]:
            thumbnail_name = thumbnails["name"]
            thumbnail = Thumbnail(
                source=open(image_source, "rb"),
                height=thumbnails["size"],
                width=thumbnails["size"],
            )
            source_image = thumbnail.generate()
            path = (
                settings.MEDIA_ROOT
                + f"{picture.owner}/"
                + f"{tier.name}/"
                + f"{thumbnail_name}/"
                + picture.name
            )
            print(path)
            while os.path.exists(path):
                path = path.split(".")
                path[-2] += "_1"
                path = ".".join(path)

            with open(path, "wb") as f:
                f.write(source_image.getvalue())
            list_of_sizes_and_url.append(
                {
                    "tier_name": tier.name,
                    "data": {"size": thumbnails["name"], "url": path},
                }
            )
    return list_of_sizes_and_url
