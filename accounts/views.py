from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()   
            return redirect('login')
        else:
            print(form.errors)
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})
def login_view(request):

    error = None

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')

        user = authenticate(request, username=username, password=password)

        if user is not None:

            # ROLE CHECK
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


# ---------------- LOGOUT ----------------
def logout_view(request):
    logout(request)
    return redirect('login')