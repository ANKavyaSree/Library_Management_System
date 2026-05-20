from django.db import models

from books.models import Book

from accounts.models import CustomUser


class IssueBook(models.Model):

    STATUS_CHOICES = [

        ('pending', 'Pending'),

        ('approved', 'Approved'),

        ('rejected', 'Rejected'),

        ('return_requested', 'Return Requested'),

        ('returned', 'Returned'),

        ('damaged', 'Damaged'),

        ('lost', 'Lost'),
    ]

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE
    )

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='pending'
    )

    request_date = models.DateField(
        auto_now_add=True
    )

    issue_date = models.DateField(
        null=True,
        blank=True
    )

    due_date = models.DateField(
        null=True,
        blank=True
    )

    rejection_reason = models.TextField(
        blank=True,
        null=True
    )

    # ADD THIS

    return_reason = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):

        return f"{self.user.username} - {self.book.title}"