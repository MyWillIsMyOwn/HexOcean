from django.conf import settings
from django.contrib.auth.models import User, Group
import requests, os
from rest_framework import serializers, reverse
from .models import Image, Account, Tier
from PIL import Image as PILImage
from io import BytesIO
from urllib.parse import urljoin
from imagekit.processors import ResizeToFill
from imagekit import ImageSpec

# from django.urls import reverse
class Thumbnail(ImageSpec):
    format = "JPEG"
    options = {"quality": 90}

    def __init__(self, height, width, *args, **kwargs):
        super(type(self), self).__init__(*args, **kwargs)
        self.processors = [ResizeToFill(height=height, width=width)]


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "groups"]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]


class ImageSerializer(serializers.HyperlinkedModelSerializer):
    # small_thumbnail = serializers.ImageField(read_only=True)
    # middle_thubmnail = serializers.ImageField(read_only=True)
    original_thubmnail = serializers.ImageField(read_only=True)
    user_account_type = serializers.CharField(
        source="owner.accounts.first.account_type", read_only=True
    )
    binary = serializers.SerializerMethodField()
    # custom_tier = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = [
            "id",
            "name",
            "original_thubmnail",
            "binary",
            "user_account_type",
        ]

    def get_custom_tier(self, obj):
        account = Account.objects.get(user=obj.owner)
        custom_tier = False
        try:
            if account.tier is not None:
                custom_tier = True
        except AttributeError:
            pass
        return custom_tier

    def to_representation(self, instance: Image):
        representation = super().to_representation(instance)
        get_user_tier = Account.objects.get(user=instance.owner)
        get_user_tier_data = get_user_tier.tier.thumbnails
        tier_name = get_user_tier.tier.name
        request = self.context.get("request")
        if not get_user_tier_data["original_link_enabled"]:
            del representation["original_thubmnail"]
        if not get_user_tier_data["expiring_links_enabled"]:
            del representation["binary"]
        representation["user_account_type"] = tier_name

        new_list = []
        for item in instance.thumbnails_data:
            if item["tier_name"] == tier_name:
                new_list.append(
                    {"url": item["data"]["url"], "size": item["data"]["size"]}
                )
        for field in get_user_tier.tier.thumbnails["thumbnails"]:
            for item in new_list:
                if item["size"] == field["name"]:
                    url = item["url"]
                    full_url = request.build_absolute_uri(url)
                    full_url = full_url.replace(str(settings.BASE_DIR), "")
                    representation[field["name"]] = full_url
        return representation

    def get_binary(self, obj):
        request = self.context.get("binary_request") or self.context.get("request")
        if request is None:
            return None
        url = reverse.reverse("binary_image", kwargs={"id": obj.id}, request=request)
        return f"{url}"
