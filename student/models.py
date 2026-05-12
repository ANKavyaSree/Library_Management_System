from django.db import models
from django.conf import settings
from books.models import Book
from datetime import date
class BorrowBook(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    returned = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.student.username} - {self.book.title}"
class Fine(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    borrow = models.ForeignKey(BorrowBook, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    paid = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.student.username} - ₹{self.amount}"