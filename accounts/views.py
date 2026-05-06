from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Student
from django.views.decorators.csrf import csrf_exempt

# REGISTER
def register_view(request):

    # ✅ SHOW PAGE (GET REQUEST)
    if request.method == "GET":
        return render(request, "register.html")

    # ✅ HANDLE FORM (POST REQUEST)
    if request.method == "POST":
        try:
            username = request.POST.get("username")
            password = request.POST.get("password")

            if not username or not password:
                return JsonResponse({
                    "status": "error",
                    "message": "Missing fields"
                })

            if User.objects.filter(username=username).exists():
                return JsonResponse({
                    "status": "error",
                    "message": "Username already exists"
                })

            user = User.objects.create_user(username=username, password=password)
            user.is_staff = False
            user.save()

            return JsonResponse({
                "status": "success",
                "message": "Registered successfully"
            })

        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": str(e)
            })


# LOGIN
@csrf_exempt
def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")
        role = request.POST.get("role")

        user = authenticate(request, username=username, password=password)

        if user is not None:

            login(request, user)

            # 🔥 STUDENT LOGIN
            if role == "student" and not user.is_staff:
                return JsonResponse({
                    "status": "success",
                    "role": "student",
                    "redirect": "/student-dashboard/"
                })

            # 🔥 ADMIN LOGIN
            elif role == "admin" and user.is_staff:
                return JsonResponse({
                    "status": "success",
                    "role": "admin",
                    "redirect": "/admin-dashboard/"
                })

            # ❌ ROLE MISMATCH
            else:
                return JsonResponse({
                    "status": "error",
                    "message": "Invalid role selected"
                })

        # ❌ WRONG CREDENTIALS
        return JsonResponse({
            "status": "error",
            "message": "Invalid credentials"
        })

    return render(request, "login.html")


# LOGOUT
def logout_view(request):
    logout(request)
    return redirect('login')


# STUDENT DASHBOARD
@login_required
def student_dashboard(request):

    student = Student.objects.filter(user=request.user).first()

    return render(request, "student_dashboard.html", {
        "student": student
    })


# ADMIN DASHBOARD
@login_required
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

def profile_view(request):
    return render(request, "profile.html")


def save_profile(request):

    if request.method == "POST":

        try:
            print("BEFORE SAVE")

            student, created = Student.objects.get_or_create(user=request.user)

            student.name = request.POST.get("name")
            student.mobile = request.POST.get("mobile")
            student.email = request.POST.get("email")
            student.register_number = request.POST.get("register_number")
            student.board = request.POST.get("board")

            dob = request.POST.get("dob")

            # 🔥 SAFE DOB HANDLING
            if dob:
                student.dob = dob
            else:
                student.dob = None

            student.status = "active"

            student.save()

            print("AFTER SAVE")

            return JsonResponse({
                "status": "success",
                "board": student.board
            })

        except Exception as e:
            print("ERROR:", e)

            return JsonResponse({
                "status": "error",
                "message": str(e)
            })

    # 🔥 IMPORTANT: always return response
    return JsonResponse({
        "status": "error",
        "message": "Invalid request"
    })
        
def cbse_view(request):
    return render(request, "cbse.html")

def kerala_view(request):
    return render(request, "kerala.html")