from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class Image(models.Model):
    picture = models.ImageField(upload_to="images")
    owner = models.ForeignKey(User, related_name="owner", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    small_thumbnail = ImageSpecField(
        source="picture",
        processors=[ResizeToFill(200, 200)],
        format="JPEG",
        options={"quality": 60},
    )
    middle_thubmnail = ImageSpecField(
        source="picture",
        processors=[ResizeToFill(400, 400)],
        format="JPEG",
        options={"quality": 60},
    )
    original_thubmnail = ImageSpecField(
        source="picture",
        format="JPEG",
        options={"quality": 60},
    )


class Account(models.Model):
    ACCOUNT_TYPES = (
        ("Basic", "Basic"),
        ("Premium", "Premium"),
        ("Enterprise", "Enterprise"),
    )
    user = models.ForeignKey(User, related_name="accounts", on_delete=models.CASCADE)
    account_type = models.CharField(
        max_length=20, choices=ACCOUNT_TYPES, default="Basic"
    )

    def clean(self):
        if Account.objects.filter(user=self.user).exclude(pk=self.pk).exists():
            raise ValueError("This user already has an account")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "account_type"], name="unique_account_for_owner"
            )
        ]
