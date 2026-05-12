from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .forms import RegisterForm
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
@csrf_exempt
def register_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        form = RegisterForm(data)
        if form.is_valid():
            form.save()
            return JsonResponse({
                'status': True,
                'message': 'User registered successfully'
            })
        return JsonResponse({
            'status': False,
            'errors': form.errors
        })
    return JsonResponse({'message': 'POST method required'})
# ---------------- LOGIN API ----------------
@csrf_exempt
def login_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        role = data.get('role')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.role == role:
                login(request, user)
                return JsonResponse({
                    'status': True,
                    'message': 'Login successful',
                    'username': user.username,
                    'role': user.role
                })
            return JsonResponse({
                'status': False,
                'message': 'Selected role is incorrect'
            })
        return JsonResponse({
            'status': False,
            'message': 'Invalid username or password'
        })
    return JsonResponse({'message': 'POST method required'})
# ---------------- LOGOUT API ----------------
@csrf_exempt
def logout_api(request):
    logout(request)
    return JsonResponse({
        'status': True,
        'message': 'Logout successful'
    })
