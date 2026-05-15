from rest_framework import serializers
from .models import IssueBook


class IssueBookSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        source='user.username',
        read_only=True
    )

    role = serializers.CharField(
        source='user.role',
        read_only=True
    )

    book_title = serializers.CharField(
        source='book.title',
        read_only=True
    )

    class Meta:
        model = IssueBook

        fields = [
            'id',
            'user',
            'username',
            'role',
            'book',
            'book_title',
            'request_date',
            'issue_date',
            'due_date',
            'status'
        ]

        read_only_fields = [
            'request_date',
            'issue_date',
            'due_date',
            'status'
        ]