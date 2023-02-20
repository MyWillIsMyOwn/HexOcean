from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class Image(models.Model):
    picture = models.ImageField(upload_to="images")
    owner = models.ForeignKey(User, related_name="owner", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    thumbnail = ImageSpecField(
        source="picture",
        processors=[ResizeToFill(200, 200)],
        format="JPEG",
        options={"quality": 60},
    )
