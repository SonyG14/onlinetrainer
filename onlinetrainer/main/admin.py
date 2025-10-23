from django.contrib import admin
from .models import CustomUser
from .models import Review

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "is_active", "is_staff")

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'created_at')