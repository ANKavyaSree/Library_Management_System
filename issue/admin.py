from django.contrib import admin
from .models import IssueBook


@admin.register(IssueBook)
class IssueBookAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'book',
        'status',
        'request_date',
        'issue_date',
        'due_date',
    )

    list_filter = (
        'status',
        'request_date',
    )

    search_fields = (
        'user__username',
        'book__title',
        'book__author',
    )

    ordering = ('-request_date',)

    list_per_page = 20