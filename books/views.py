from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, Category
from .forms import BookForm, CategoryForm
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