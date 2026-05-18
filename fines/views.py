from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

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


# ======================================
# MY FINES
# ======================================

@login_required
def my_fines(request):

    # ONLY STUDENTS CAN HAVE FINES

    if request.user.role != 'student':

        return render(
            request,
            'fines/my_fines.html'
        )

    fines = Fine.objects.filter(
        user=request.user
    ).order_by('-created_at')

    unpaid_fines = Fine.objects.filter(
        user=request.user,
        paid=False
    )

    total_amount = sum(
        fine.amount for fine in unpaid_fines
    )

    context = {
        'fines': fines,
        'total_amount': total_amount
    }

    return render(
        request,
        'fines/my_fines.html',
        context
    )


# ======================================
# PAY FINE
# ======================================

@login_required
def pay_fine(request, fine_id):

    # TEACHERS SHOULD NOT PAY FINES

    if request.user.role != 'student':

        return redirect('my_fines')

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

    # ONLY STUDENTS CAN ACCESS

    if request.user.role != 'student':

        return Response(
            {
                'message': 'Teachers do not have fines'
            },
            status=status.HTTP_403_FORBIDDEN
        )

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

    # ONLY STUDENTS

    if request.user.role != 'student':

        return Response(
            {
                'message': 'Teachers do not have fines'
            },
            status=status.HTTP_403_FORBIDDEN
        )

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

    # ONLY STUDENTS

    if request.user.role != 'student':

        return Response(
            {
                'message': 'Teachers cannot pay fines because teachers are not fined'
            },
            status=status.HTTP_403_FORBIDDEN
        )

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
# LIBRARIAN
# ======================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_fines_api(request):

    # ONLY STUDENT FINES

    fines = Fine.objects.filter(
        user__role='student'
    ).order_by('-created_at')

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

        user = serializer.validated_data['user']

        # DO NOT ALLOW TEACHER FINES

        if user.role == 'teacher':

            return Response(
                {
                    'message': 'Teachers cannot be fined'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

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