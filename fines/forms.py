from django import forms

from .models import Fine

from accounts.models import CustomUser
from .models import Payment
class FineForm(forms.ModelForm):

    user = forms.IntegerField(

        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter Student ID'
            }
        )
    )

    class Meta:

        model = Fine

        fields = ['user', 'amount', 'reason']

        widgets = {

            'amount': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter Fine Amount'
                }
            ),

            'reason': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter Fine Reason'
                }
            ),
        }

    def clean_user(self):

        user_id = self.cleaned_data['user']

        try:

            student = CustomUser.objects.get(
                id=user_id,
                role='student'
            )

            return student

        except CustomUser.DoesNotExist:

            raise forms.ValidationError(
                "Student with this ID does not exist."
            )
class PaymentForm(forms.ModelForm):

    class Meta:

        model = Payment

        fields = ['screenshot']