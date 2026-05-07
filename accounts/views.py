from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Student, CBSEAcademicDetails, KeralaAcademicDetails, Extracurricular, CoursePreference
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
    if request.method == "POST":

        science = float(request.POST['science'])
        social_science = float(request.POST['social_science'])
        maths = float(request.POST['maths'])
        english = float(request.POST['english'])
        language = float(request.POST['language'])
        it = float(request.POST['it'])

        total = (
            science +
            social_science +
            maths +
            english +
            language +
            it 
        )

        student = request.user.student

        CBSEAcademicDetails.objects.create(
            student=student,
            science=science,
            social_science=social_science,
            maths=maths,
            english=english,
            language=language,
            it=it,
            total=total
        )

        return redirect('extracurricular')

    return render(request, 'cbse.html')



grade_map = {
    "A+": 95,
    "A": 85,
    "B+": 75,
    "B": 65,
    "C+": 55,
    "C": 45,
    "D+": 35,
    "D": 25,
}


def kerala_view(request):
    if request.method == "POST":

        language1 = request.POST['language1']
        language2 = request.POST['language2']

        english = request.POST['english']
        hindi = request.POST['hindi']

        social_science = request.POST['social_science']

        physics = request.POST['physics']
        chemistry = request.POST['chemistry']
        biology = request.POST['biology']

        mathematics = request.POST['mathematics']
        it = request.POST['it']

        total = (
            grade_map[language1] +
            grade_map[language2] +
            grade_map[english] +
            grade_map[hindi] +
            grade_map[social_science] +
            grade_map[physics] +
            grade_map[chemistry] +
            grade_map[biology] +
            grade_map[mathematics] +
            grade_map[it]
        )

        student = request.user.student

        KeralaAcademicDetails.objects.create(

            student=student,

            language1=language1,
            language2=language2,

            english=english,
            hindi=hindi,

            social_science=social_science,

            physics=physics,
            chemistry=chemistry,
            biology=biology,

            mathematics=mathematics,
            it=it,

            total=total
        )

        return redirect('extracurricular')

    return render(request, 'kerala.html')



def extracurricular(request):

    student = request.user.student

    if request.method == "POST":

        none_activity = 'none_activity' in request.POST

        Extracurricular.objects.create(

            student=student,

            # NCC
            ncc_nss_spc=False if none_activity else 'ncc_nss_spc' in request.POST,
            ncc_certificate=None if none_activity else request.FILES.get('ncc_certificate'),

            # Sports
            sports_district=False if none_activity else 'sports_district' in request.POST,
            sports_state=False if none_activity else 'sports_state' in request.POST,
            sports_national=False if none_activity else 'sports_national' in request.POST,
            sports_certificate=None if none_activity else request.FILES.get('sports_certificate'),

            # Youth Festival
            youth_district=False if none_activity else 'youth_district' in request.POST,
            youth_state=False if none_activity else 'youth_state' in request.POST,
            youth_national=False if none_activity else 'youth_national' in request.POST,
            youth_certificate=None if none_activity else request.FILES.get('youth_certificate'),
        )

        return redirect('course_preference')

    return render(request, 'extracurricular.html')


def course_preference(request):

    student = request.user.student

    if request.method == "POST":

        pref1 = request.POST['pref1']
        pref2 = request.POST['pref2']
        pref3 = request.POST['pref3']

        CoursePreference.objects.create(

            student=student,

            pref1=pref1,
            pref2=pref2,
            pref3=pref3
        )

        return redirect('student_dashboard')

    return render(request, 'course_preference.html')
