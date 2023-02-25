from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
from imagekit.models import ImageSpecField


class Image(models.Model):
    picture = models.ImageField(upload_to="images")
    owner = models.ForeignKey(User, related_name="owner", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    original_thubmnail = ImageSpecField(
        source="picture",
        format="JPEG",
        options={"quality": 60},
    )
    link_date_expiration = models.DateTimeField(default=datetime.now())
    binary_image = models.BinaryField(null=True)
    thumbnails_data = models.JSONField(null=True)

    def __str__(self):
        return f"Image owner: {self.owner}"


class Tier(models.Model):
    name = models.CharField(max_length=100)
    thumbnails = models.JSONField(
        default={
            "thumbnails": [
                {"name": "small", "size": 200},
                {"name": "big", "size": 400},
                {"name": "huge", "size": 800},
            ],
            "original_link_enabled": True,
            "expiring_links_enabled": False,
        }
    )

    def clean(self):
        # Check if all required fields are present in the dictionary
        required_fields = [
            "thumbnails",
            "original_link_enabled",
            "expiring_links_enabled",
        ]
        for field in required_fields:
            if field not in self.thumbnails:
                raise ValidationError(
                    f"{field} is missing from the thumbnails dictionary."
                )

        # Check if thumbnails field is properly constructed
        for thumbnail in self.thumbnails["thumbnails"]:
            if not all(key in thumbnail for key in ["name", "size"]):
                raise ValidationError("Invalid thumbnail dictionary.")
            if not isinstance(thumbnail.get("size"), int):
                raise ValidationError("Thumbnail size must be an integer.")

        super().clean()

    def __str__(self):
        return f"Tier name: {self.name}"


class Account(models.Model):

    user = models.ForeignKey(User, related_name="accounts", on_delete=models.CASCADE)
    tier = models.ForeignKey(
        Tier, related_name="accounts", on_delete=models.CASCADE, null=True, blank=True
    )

    def clean(self):
        if Account.objects.filter(user=self.user).exclude(pk=self.pk).exists():
            raise ValueError("This user already has an account")

    def __str__(self):
        return f"User: {self.user}"
