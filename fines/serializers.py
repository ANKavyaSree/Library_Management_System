from rest_framework import serializers
from .models import Fine


class FineSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        source='user.username',
        read_only=True
    )

    class Meta:
        model = Fine

        fields = [
            'id',
            'user',
            'username',
            'amount',
            'reason',
            'paid',
            'created_at'
        ]

        read_only_fields = [
            'created_at'
        ]