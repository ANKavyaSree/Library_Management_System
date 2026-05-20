from django.db import models
from django.conf import settings
from accounts.models import CustomUser
class Fine(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    amount = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )
    reason = models.CharField(max_length=255)
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.username} - ₹{self.amount}"
    
class Payment(models.Model):

    fine = models.ForeignKey(
        Fine,
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE
    )

    screenshot = models.ImageField(
        upload_to='payments/'
    )

    paid_on = models.DateTimeField(
        auto_now_add=True
    )

    is_verified = models.BooleanField(
        default=False
    )

    def __str__(self):

        return f"{self.user.username} Payment"