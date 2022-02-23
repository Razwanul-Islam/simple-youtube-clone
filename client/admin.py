from django.contrib import admin
from .models import CustomUser, Video
from django.contrib.auth.admin import UserAdmin

class VideoAdmin(admin.ModelAdmin):
    list_display = ['title','uploaded_at']
admin.site.register(CustomUser,UserAdmin)
admin.site.register(Video,VideoAdmin)
# Register your models here.
