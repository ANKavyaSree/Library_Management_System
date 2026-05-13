from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Fine
@login_required
def my_fines(request):
    fines = Fine.objects.filter(
        user=request.user
    )
    total_unpaid = Fine.objects.filter(
        user=request.user,
        paid=False
    )
    total_amount = sum(f.amount for f in total_unpaid)
    return render(request, 'fines/my_fines.html', {
        'fines': fines,
        'total_amount': total_amount
    })
@login_required
def pay_fine(request, fine_id):
    fine = get_object_or_404(
        Fine,
        id=fine_id,
        user=request.user
    )
    fine.paid = True
    fine.save()
    return redirect('my_fines')