from django.contrib import admin
from .models import Image, Account, Tier

# # Register your models here.
admin.site.register(Image)
admin.site.register(Account)
admin.site.register(Tier)
