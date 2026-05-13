from django.contrib import admin
from .models import Fine


@admin.register(Fine)
class FineAdmin(admin.ModelAdmin):
    list_display = ['user','amount','reason','paid','created_at']
    list_filter = ['paid']
    search_fields = ['user__username','reason' ]