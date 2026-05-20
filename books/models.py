from django.db import models


class Category(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    def __str__(self):

        return self.name


class Book(models.Model):

    title = models.CharField(
        max_length=200
    )

    author = models.CharField(
        max_length=150
    )

    isbn = models.CharField(
        max_length=20,
        unique=True
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )

    # NEW FIELD

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    available = models.PositiveIntegerField(
        default=1
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    added_on = models.DateTimeField(
        auto_now_add=True
    )

    def save(self, *args, **kwargs):

        if not self.pk:

            self.available = self.quantity

        super().save(*args, **kwargs)

    def __str__(self):

        return self.title