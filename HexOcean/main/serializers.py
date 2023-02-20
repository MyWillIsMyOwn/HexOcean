from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Image, Account


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "groups"]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]


class ImageSerializer(serializers.HyperlinkedModelSerializer):
    small_thumbnail = serializers.ImageField(read_only=True)
    middle_thubmnail = serializers.ImageField(read_only=True)
    original_thubmnail = serializers.ImageField(read_only=True)
    user_account_type = serializers.CharField(
        source="owner.accounts.first.account_type", read_only=True
    )

    class Meta:
        model = Image
        fields = [
            "id",
            "name",
            "small_thumbnail",
            "middle_thubmnail",
            "original_thubmnail",
            "uploaded_at",
            "user_account_type",
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        account_type = representation["user_account_type"]
        print("aaaaaaa", representation)
        print(type(representation))
        if account_type == "Basic":
            del representation["middle_thubmnail"]
            del representation["original_thubmnail"]
        elif account_type == "Premium":
            del representation["original_thubmnail"]

        return representation
