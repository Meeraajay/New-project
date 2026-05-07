from django.shortcuts import render
from .models import AdmissionResult

from accounts.models import (
    Student,
    CBSEAcademicDetails,
    KeralaAcademicDetails,
    Extracurricular,
    CoursePreference
)

# =========================
# STREAM TIE BREAKER LOGIC
# =========================
def get_stream_score(student, course):

    cbse = CBSEAcademicDetails.objects.filter(student=student).first()
    kerala = KeralaAcademicDetails.objects.filter(student=student).first()

    # CS / BIO-MATHS
    if course in ["Computer Science", "Bio-Mathematics"]:

        if cbse:
            return cbse.science + cbse.maths

        elif kerala:
            return kerala.physics + kerala.chemistry + kerala.biology + kerala.maths

    # COMMERCE
    elif course == "Commerce":

        if cbse:
            return cbse.maths + cbse.social_science

        elif kerala:
            return kerala.maths + kerala.social_science

    # HUMANITIES
    elif course == "Humanities":

        if cbse:
            return cbse.social_science   # FIXED (was social ❌)

        elif kerala:
            return kerala.social_science  # FIXED (was social ❌)

    return 0


# =========================
# MAIN FUNCTION
# =========================
def calculate_results(request=None):   # FIX: allows terminal run

    AdmissionResult.objects.all().delete()

    students = Student.objects.all()

    for student in students:

        bonus_mark = 0
        academic_score = 0

        cbse = CBSEAcademicDetails.objects.filter(student=student).first()
        kerala = KeralaAcademicDetails.objects.filter(student=student).first()

        # skip incomplete students
        if not cbse and not kerala:
            print(f"SKIPPED: {student.name} (no academic data)")
            continue

        # academic normalization
        if cbse:
            academic_score = (cbse.total / 600) * 100
        else:
            academic_score = (kerala.total / 1000) * 100

        # bonus
        extra = Extracurricular.objects.filter(student=student).first()

        if extra:

            if extra.sports_national:
                bonus_mark += 15
            elif extra.sports_state:
                bonus_mark += 10
            elif extra.sports_district:
                bonus_mark += 5

            if extra.youth_national:
                bonus_mark += 15
            elif extra.youth_state:
                bonus_mark += 10
            elif extra.youth_district:
                bonus_mark += 5

            if extra.ncc_nss_spc:
                bonus_mark += 5

        if bonus_mark > 20:
            bonus_mark = 20

        final_score = academic_score + bonus_mark

        preference = CoursePreference.objects.filter(student=student).first()

        if not preference:
            print(f"SKIPPED: {student.name} (no preferences)")
            continue

        courses = [preference.pref1, preference.pref2, preference.pref3]

        for course in courses:

            stream_score = get_stream_score(student, course)

            AdmissionResult.objects.update_or_create(
                student=student,
                course=course,
                defaults={
                    "index_mark": academic_score,
                    "bonus_mark": bonus_mark,
                    "final_score": final_score,
                    "stream_score": stream_score
                }
            )

    # =========================
    # RANKING
    # =========================
    course_list = [
        "Computer Science",
        "Bio-Mathematics",
        "Commerce",
        "Humanities"
    ]

    for course in course_list:

        results = AdmissionResult.objects.filter(course=course).order_by(
            '-final_score',
            '-stream_score',
            '-bonus_mark',
            'student_id'
        )

        rank = 1

        for result in results:
            result.rank = rank
            result.save()
            rank += 1

    print("CALCULATION COMPLETE ✔")

    if request:
        return render(request, 'calculation_done.html')