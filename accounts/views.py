from django.shortcuts import (
    render,
    redirect
)

from django.contrib.auth import (
    authenticate,
    login,
    logout
)

from django.contrib import messages

from .forms import RegisterForm

from rest_framework.decorators import (
    api_view,
    permission_classes
)

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)

from rest_framework.response import Response

from rest_framework import status

from rest_framework_simplejwt.tokens import (
    RefreshToken
)

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from django.http import JsonResponse
def check_session(request):

    return JsonResponse({
        'authenticated': request.user.is_authenticated
    })

def home(request):

    return render(
        request,
        'home.html'
    )

@login_required
def profile_view(request):

    return render(
        request,
        'accounts/profile.html'
    )


def csrf_error(request, reason=""):

    return redirect('login')

# ==========================================
# ROLE BASED REDIRECT
# ==========================================

def redirect_by_role(user):

    role = getattr(user, 'role', None)

    if role == 'student':

        return redirect('/student/dashboard/')

    elif role == 'teacher':

        return redirect('/teacher/dashboard/')

    elif role == 'librarian':

        return redirect('/librarian/dashboard/')

    return redirect('login')


# ==========================================
# GENERATE JWT TOKENS
# ==========================================

def get_tokens_for_user(user):

    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


# ==========================================
# REGISTER VIEW
# ==========================================

def register_view(request):

    # block register if logged in

    if request.user.is_authenticated:

        return redirect_by_role(request.user)

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Registration successful'
            )

            return redirect('login')

    else:

        form = RegisterForm()

    return render(
        request,
        'accounts/register.html',
        {
            'form': form
        }
    )


# ==========================================
# LOGIN VIEW
# ==========================================


def login_view(request):

    # IF USER ALREADY LOGGED IN
    # DO NOT ALLOW ANOTHER LOGIN

    if request.user.is_authenticated:

        messages.warning(
            request,
            f"{request.user.username} is already logged in. Please logout first."
        )

        # REDIRECT TO THEIR OWN DASHBOARD

        if request.user.role == 'student':
            return redirect('student_dashboard')

        elif request.user.role == 'teacher':
            return redirect('teacher_dashboard')

        elif request.user.role == 'librarian':
            return redirect('librarian_dashboard')

    # LOGIN PROCESS

    if request.method == 'POST':

        username = request.POST.get('username')

        password = request.POST.get('password')

        role = request.POST.get('role')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            # CHECK ROLE MATCH

            if user.role != role:

                messages.error(
                    request,
                    "Selected role does not match account."
                )

                return redirect('login')

            # LOGIN USER

            login(request, user)

            # ROLE BASED REDIRECT

            if user.role == 'student':
                return redirect('student_dashboard')

            elif user.role == 'teacher':
                return redirect('teacher_dashboard')

            elif user.role == 'librarian':
                return redirect('librarian_dashboard')

        else:

            messages.error(
                request,
                "Invalid username or password"
            )

    return render(
        request,
        'accounts/login.html'
    )
# ==========================================
# LOGOUT VIEW
# ==========================================

def logout_view(request):

    logout(request)

    messages.success(
        request,
        'Logout successful'
    )

    return redirect('home')


# ==========================================
# REGISTER API
# ==========================================

@api_view(['POST'])
@permission_classes([AllowAny])

def register_api(request):

    if request.user.is_authenticated:

        return Response(
            {
                'status': False,
                'message': 'Already logged in'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    form = RegisterForm(request.data)

    if form.is_valid():

        user = form.save()

        return Response(
            {
                'status': True,
                'message': 'User registered successfully',
                'user_id': user.id
            },
            status=status.HTTP_201_CREATED
        )

    return Response(
        {
            'status': False,
            'errors': form.errors
        },
        status=status.HTTP_400_BAD_REQUEST
    )


# ==========================================
# LOGIN API
# ==========================================

@api_view(['POST'])
@permission_classes([AllowAny])

def login_api(request):

    if request.user.is_authenticated:

        tokens = get_tokens_for_user(request.user)

        return Response(
            {
                'status': True,
                'message': 'Already logged in',
                'refresh': tokens['refresh'],
                'access': tokens['access'],
                'user': {
                    'id': request.user.id,
                    'username': request.user.username,
                    'email': request.user.email,
                    'role': getattr(request.user, 'role', None)
                }
            }
        )

    username = request.data.get('username')

    password = request.data.get('password')

    role = request.data.get('role')

    user = authenticate(
        request,
        username=username,
        password=password
    )

    if user is not None:

        if getattr(user, 'role', None) != role:

            return Response(
                {
                    'status': False,
                    'message': 'Invalid role selected'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        login(request, user)

        tokens = get_tokens_for_user(user)

        return Response(
            {
                'status': True,
                'message': 'Login successful',

                'refresh': tokens['refresh'],
                'access': tokens['access'],

                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'role': getattr(user, 'role', None)
                }
            },
            status=status.HTTP_200_OK
        )

    return Response(
        {
            'status': False,
            'message': 'Invalid credentials'
        },
        status=status.HTTP_401_UNAUTHORIZED
    )


# ==========================================
# PROFILE API
# ==========================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])

def profile_api(request):

    user = request.user

    return Response(
        {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': getattr(user, 'role', None)
        }
    )


# ==========================================
# LOGOUT API
# ==========================================

@api_view(['POST'])
@permission_classes([IsAuthenticated])

def logout_api(request):

    logout(request)

    return Response(
        {
            'status': True,
            'message': 'Logout successful'
        },
        status=status.HTTP_200_OK
    )