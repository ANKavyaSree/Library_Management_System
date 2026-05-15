from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .forms import RegisterForm
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    permission_classes
)
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)

from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    RegisterSerializer,
    LoginSerializer
)
# ---------------- REGISTER VIEW ----------------
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            print(form.errors)
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})
# ---------------- LOGIN VIEW ----------------
def login_view(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.role == role:
                login(request, user)
                if role == 'student':
                    return redirect('student_dashboard')
                elif role == 'teacher':
                    return redirect('teacher_dashboard')
                elif role == 'librarian':
                    return redirect('librarian_dashboard')
            else:
                error = "Selected role is incorrect"
        else:
            error = "Invalid username or password"
    return render(request, 'accounts/login.html', {'error': error})
# ---------------- LOGOUT VIEW ----------------
def logout_view(request):
    logout(request)
    return redirect('login')
# ======================================================
#                     API VIEWS
# ======================================================
# ---------------- REGISTER API ----------------

# ====================================
# REGISTER API
# ====================================
@api_view(['POST'])
@permission_classes([AllowAny])
def register_api(request):

    serializer = RegisterSerializer(
        data=request.data
    )

    if serializer.is_valid():

        serializer.save()

        return Response(
            {
                'status': True,
                'message': 'User registered successfully'
            },
            status=status.HTTP_201_CREATED
        )

    return Response(
        {
            'status': False,
            'errors': serializer.errors
        },
        status=status.HTTP_400_BAD_REQUEST
    )


# ====================================
# LOGIN API
# ====================================

@api_view(['POST'])
@permission_classes([AllowAny])
def login_api(request):

    serializer = LoginSerializer(
        data=request.data
    )

    if serializer.is_valid():

        user = serializer.validated_data['user']

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                'status': True,
                'message': 'Login successful',

                'refresh': str(refresh),
                'access': str(refresh.access_token),

                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'role': user.role
                }
            }
        )

    return Response(
        {
            'status': False,
            'errors': serializer.errors
        },
        status=status.HTTP_400_BAD_REQUEST
    )


# ====================================
# PROFILE API
# ====================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_api(request):

    user = request.user

    return Response(
        {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role
        }
    )

@api_view(['POST'])
def logout_api(request):

    logout(request)

    return Response({
        'status': True,
        'message': 'Logout successful'
    })