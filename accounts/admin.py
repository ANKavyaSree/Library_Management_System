from django.contrib import admin
from .models import CustomUser


# @admin.register(CustomUser)
# class CustomUserAdmin(admin.ModelAdmin):

#     list_display = ('id', 'username', 'email', 'role', 'is_staff')

#     list_filter = ('role',)

#     search_fields = ('username', 'email')

#     def get_queryset(self, request):
#         qs = super().get_queryset(request)
#         return qs.filter(role='student')  # show only students

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'role')