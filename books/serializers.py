from rest_framework import serializers
from .models import Book, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class BookSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(
        source='category.name',
        read_only=True
    )

    class Meta:
        model = Book

        fields = [
            'id',
            'title',
            'author',
            'isbn',
            'category',
            'category_name',
            'quantity',
            'available',
            'description',
            'added_on'
        ]

        read_only_fields = [
            'available',
            'added_on'
        ]