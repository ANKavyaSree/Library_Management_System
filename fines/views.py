from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Fine
from rest_framework.decorators import (
    api_view,
    permission_classes
)
from rest_framework.permissions import (
    IsAuthenticated
)
from .serializers import FineSerializer
from rest_framework.response import Response
from rest_framework import status
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


# ======================================
# MY FINES API
# ======================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_fines_api(request):

    fines = Fine.objects.filter(
        user=request.user
    ).order_by('-created_at')

    serializer = FineSerializer(
        fines,
        many=True
    )

    return Response(serializer.data)


# ======================================
# UNPAID FINES API
# ======================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def unpaid_fines_api(request):

    fines = Fine.objects.filter(
        user=request.user,
        paid=False
    ).order_by('-created_at')

    serializer = FineSerializer(
        fines,
        many=True
    )

    return Response(serializer.data)


# ======================================
# PAY FINE API
# ======================================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def pay_fine_api(request, pk):

    fine = get_object_or_404(
        Fine,
        id=pk,
        user=request.user
    )

    if fine.paid:
        return Response(
            {
                'message': 'Fine already paid'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    fine.paid = True
    fine.save()

    return Response(
        {
            'message': 'Fine paid successfully'
        }
    )


# ======================================
# ALL FINES API
# LIBRARIIAN
# ======================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_fines_api(request):

    fines = Fine.objects.all().order_by('-created_at')

    serializer = FineSerializer(
        fines,
        many=True
    )

    return Response(serializer.data)


# ======================================
# ADD FINE API
# LIBRARIAN
# ======================================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_fine_api(request):

    serializer = FineSerializer(
        data=request.data
    )

    if serializer.is_valid():
        serializer.save()

        return Response(
            {
                'message': 'Fine added successfully',
                'data': serializer.data
            },
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )