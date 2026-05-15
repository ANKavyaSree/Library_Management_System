from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, Category
from .forms import BookForm, CategoryForm
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    BookSerializer,
    CategorySerializer
)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny
)


def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_book')
    else:
        form = CategoryForm()

    return render(request, 'books/add_category.html', {'form': form})
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('search_book')
    else:
        form = BookForm()

    return render(request, 'books/add_book.html', {'form': form})
def edit_book(request, id):
    book = get_object_or_404(Book, id=id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_details', id=book.id)
    else:
        form = BookForm(instance=book)
    return render(request, 'books/edit_book.html', {'form': form})
def search_book(request):
    query = request.GET.get('q')
    category_id = request.GET.get('category')

    books = Book.objects.all()
    categories = Category.objects.all()

    if query:
        books = books.filter(title__icontains=query)

    if category_id:
        books = books.filter(category_id=category_id)

    return render(request, 'books/search_book.html', {
        'books': books,
        'categories': categories,
        'query': query
    })
def book_details(request, id):
    book = get_object_or_404(Book, id=id)
    return render(request, 'books/book_details.html', {'book': book})
# =====================================
# CATEGORY APIs
# =====================================

@api_view(['GET'])
@permission_classes([AllowAny])
def category_list_api(request):

    categories = Category.objects.all()

    serializer = CategorySerializer(
        categories,
        many=True
    )

    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_category_api(request):

    serializer = CategorySerializer(
        data=request.data
    )

    if serializer.is_valid():
        serializer.save()

        return Response(
            {
                'message': 'Category added successfully',
                'data': serializer.data
            },
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


# =====================================
# BOOK APIs
# =====================================

@api_view(['GET'])
@permission_classes([AllowAny])
def book_list_api(request):

    books = Book.objects.all().order_by('-added_on')

    query = request.GET.get('q')
    category = request.GET.get('category')

    if query:
        books = books.filter(
            title__icontains=query
        )

    if category:
        books = books.filter(
            category_id=category
        )

    serializer = BookSerializer(
        books,
        many=True
    )

    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def book_detail_api(request, pk):

    book = get_object_or_404(
        Book,
        pk=pk
    )

    serializer = BookSerializer(book)

    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_book_api(request):

    serializer = BookSerializer(
        data=request.data
    )

    if serializer.is_valid():
        serializer.save()

        return Response(
            {
                'message': 'Book added successfully',
                'data': serializer.data
            },
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_book_api(request, pk):

    book = get_object_or_404(
        Book,
        pk=pk
    )

    serializer = BookSerializer(
        book,
        data=request.data
    )

    if serializer.is_valid():
        serializer.save()

        return Response(
            {
                'message': 'Book updated successfully',
                'data': serializer.data
            }
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_book_api(request, pk):

    book = get_object_or_404(
        Book,
        pk=pk
    )

    book.delete()

    return Response(
        {
            'message': 'Book deleted successfully'
        }
    )