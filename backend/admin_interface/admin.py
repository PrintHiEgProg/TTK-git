from django.contrib import admin
from .models import Client, Intent

# Register your models here.
admin.site.register(Client)
admin.site.register(Intent)