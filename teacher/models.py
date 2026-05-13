from django.db import models
from django.conf import settings
from books.models import Book
class TeacherBorrowBook(models.Model):
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE
    )
    borrow_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    returned = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.teacher.username} - {self.book.title}"